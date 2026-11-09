from __future__ import annotations

import asyncio
import logging
import re
import time
import uuid
from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta

from app.config import Settings
from app.coolify import CoolifyClient, CoolifyError
from app.format import Button, escape_html, format_brt, short_commit
from app.store import Store
from app.telegram import TelegramClient, TelegramError

LOGGER = logging.getLogger(__name__)

DENIED = "⛔ <b>Acesso negado.</b> Este usuário ou chat não está autorizado a usar o bot."
UNKNOWN = "Comando não reconhecido. Use /ajuda para ver os comandos disponíveis."
COOLIFY_DOWN = "⚠️ Não foi possível consultar o Coolify agora. Tente novamente em instantes."

HELP = """🤖 <b>Relay Coolify → Telegram</b>

<b>Consultas</b>
/status — resumo do Coolify
/apps — lista de aplicações
/app &lt;nome|uuid&gt; — ficha da aplicação
/deploys [app] — últimos deploys
/logs &lt;uuid&gt; — status e link do deploy

<b>Ações</b>
/deploy &lt;app&gt; — confirma e dispara deploy
/iniciar &lt;app&gt; — confirma e inicia
/reiniciar &lt;app&gt; — confirma e reinicia
/parar &lt;app&gt; — confirma e para

<b>Notificações</b>
/silenciar &lt;30m|2h|off&gt; — pausa ou retoma"""

DEPLOY_ACTIVE = {"queued", "in_progress", "running"}

CONFIRM_TTL = 60.0
ACTION_RATE_LIMIT = 10.0

COMMAND_ACTION = {
    "/deploy": "deploy",
    "/iniciar": "iniciar",
    "/reiniciar": "reiniciar",
    "/parar": "parar",
}

ACTION_LABEL = {
    "deploy": "deploy",
    "iniciar": "início",
    "reiniciar": "reinício",
    "parar": "parada",
}

ACTION_METHOD = {
    "deploy": "deploy",
    "iniciar": "start",
    "reiniciar": "restart",
    "parar": "stop",
}

EXPIRED = "⌛ Confirmação expirada. Envie o comando novamente."
INVALID = "⚠️ Confirmação inválida ou expirada. Envie o comando novamente."

DURATION_RE = re.compile(r"^(\d+)([mh])$")


def _parse_duration(value: str) -> int | None:
    match = DURATION_RE.fullmatch(value.strip().lower())
    if not match:
        return None
    amount, unit = int(match.group(1)), match.group(2)
    minutes = amount if unit == "m" else amount * 60
    return minutes if 1 <= minutes <= 1440 else None


@dataclass
class PendingAction:
    action: str
    app_uuid: str
    app_name: str
    user_id: int
    chat_id: int
    expires_at: float


class Bot:
    def __init__(
        self,
        telegram: TelegramClient,
        coolify: CoolifyClient,
        store: Store,
        settings: Settings,
        clock: Callable[[], float] | None = None,
        confirm_ttl: float = CONFIRM_TTL,
        action_rate_limit: float = ACTION_RATE_LIMIT,
    ) -> None:
        self.telegram = telegram
        self.coolify = coolify
        self.store = store
        self.settings = settings
        self._clock = clock or time.monotonic
        self.confirm_ttl = confirm_ttl
        self.action_rate_limit = action_rate_limit
        self._pending: dict[str, PendingAction] = {}
        self._last_action: dict[str, float] = {}

    async def run(self, interval: float = 2.0) -> None:
        LOGGER.info(
            "Bot em long polling (usuários autorizados: %d, chats: %d)",
            len(self.settings.allowed_user_ids),
            len(self.settings.allowed_chat_ids),
        )
        while True:
            try:
                await self.poll_once()
            except Exception:
                LOGGER.exception("Falha no long polling do bot")
            await asyncio.sleep(interval)

    async def poll_once(self) -> int:
        offset_raw = self.store.meta_get("bot_offset")
        offset = int(offset_raw) if offset_raw else None
        updates = await self.telegram.get_updates(offset=offset)

        if updates:
            LOGGER.info("Bot recebeu %d atualização(ões) do Telegram", len(updates))
            newest = max(int(update.get("update_id", 0)) for update in updates)
            self.store.meta_set("bot_offset", str(newest + 1))

        for update in updates:
            await self.handle_update(update)
        return len(updates)

    async def handle_update(self, update: dict) -> None:
        callback = update.get("callback_query")
        if callback:
            LOGGER.info("Bot recebeu callback_query")
            await self._handle_callback(callback)
            return

        message = update.get("message") or {}
        text = (message.get("text") or "").strip()
        user_id = (message.get("from") or {}).get("id")
        chat_id = (message.get("chat") or {}).get("id")
        if not text or user_id is None or chat_id is None:
            LOGGER.info("Bot ignorou atualização sem texto remetente/chat")
            return

        LOGGER.info("Bot: comando=%r user_id=%s chat_id=%s", text[:50], user_id, chat_id)

        if not self._authorized(int(user_id), int(chat_id)):
            LOGGER.warning("Bot: acesso negado para user_id=%s chat_id=%s", user_id, chat_id)
            await self._reply(chat_id, DENIED)
            return

        command, _, argument = text.partition(" ")
        command = command.split("@", 1)[0].lower()
        argument = argument.strip()

        try:
            await self._dispatch(command, argument, chat_id, int(user_id))
            LOGGER.info("Bot: resposta enviada para %r", command)
        except CoolifyError as exc:
            LOGGER.warning("Consulta ao Coolify falhou: %s", exc)
            await self._reply(chat_id, COOLIFY_DOWN)
        except TelegramError as exc:
            LOGGER.warning("Envio ao Telegram falhou: %s", exc)

    def _authorized(self, user_id: int, chat_id: int) -> bool:
        users = self.settings.allowed_user_ids
        chats = self.settings.allowed_chat_ids
        if not users or not chats:
            return False
        return user_id in users and chat_id in chats

    async def _reply(
        self, chat_id: int, text: str, buttons: list[Button] | None = None
    ) -> None:
        await self.telegram.send_message(text, buttons=buttons, chat_id=chat_id)

    async def _dispatch(
        self, command: str, argument: str, chat_id: int, user_id: int
    ) -> None:
        if command in {"/ajuda", "/help", "/start"}:
            await self._reply(chat_id, HELP)
        elif command == "/status":
            await self._status(chat_id)
        elif command == "/apps":
            await self._apps(chat_id)
        elif command == "/app":
            await self._app(chat_id, argument)
        elif command == "/deploys":
            await self._deploys(chat_id, argument)
        elif command == "/logs":
            await self._logs(chat_id, argument)
        elif command == "/silenciar":
            await self._silence(chat_id, argument)
        elif command in COMMAND_ACTION:
            await self._propose_action(chat_id, user_id, COMMAND_ACTION[command], argument)
        else:
            await self._reply(chat_id, UNKNOWN)

    async def _status(self, chat_id: int) -> None:
        applications = await self.coolify.list_applications()
        servers = await self.coolify.list_servers()
        deployments = await self.coolify.list_deployments()

        running = sum(
            1 for app in applications if str(app.get("status", "")).startswith("running")
        )
        online = sum(1 for server in servers if _is_online(server))
        active = sum(
            1 for deploy in deployments if str(deploy.get("status")) in DEPLOY_ACTIVE
        )

        text = (
            "📊 <b>Status do Coolify</b>\n\n"
            f"<b>Aplicações:</b> {len(applications)} "
            f"({running} em execução, {len(applications) - running} paradas)\n"
            f"<b>Servidores:</b> {len(servers)} "
            f"({online} online, {len(servers) - online} offline)\n"
            f"<b>Deploys em andamento:</b> {active}"
        )
        await self._reply(chat_id, text)

    async def _apps(self, chat_id: int) -> None:
        applications = await self.coolify.list_applications()
        if not applications:
            await self._reply(chat_id, "Nenhuma aplicação encontrada.")
            return

        lines = [f"📦 <b>Aplicações</b> ({len(applications)})\n"]
        for app in applications[:20]:
            name = escape_html(app.get("name") or app.get("uuid") or "?")
            status = escape_html(app.get("status") or "desconhecido")
            uuid = escape_html(app.get("uuid") or "")
            lines.append(f"• <b>{name}</b> — {status}\n  <code>{uuid}</code>")
        if len(applications) > 20:
            lines.append(f"\n… e mais {len(applications) - 20}")

        await self._reply(chat_id, "\n".join(lines))

    async def _app(self, chat_id: int, argument: str) -> None:
        if not argument:
            await self._reply(chat_id, "Uso: /app &lt;nome|uuid&gt;")
            return

        app = await self._find_application(argument)
        if app is None:
            await self._reply(chat_id, f"Aplicação não encontrada: {escape_html(argument)}")
            return

        lines = [
            f"📦 <b>{escape_html(app.get('name') or app.get('uuid'))}</b>\n",
            f"<b>UUID:</b> <code>{escape_html(app.get('uuid') or '')}</code>",
            f"<b>Status:</b> {escape_html(app.get('status') or 'desconhecido')}",
        ]
        if app.get("fqdn"):
            lines.append(f"<b>Domínio:</b> {escape_html(app.get('fqdn'))}")
        if app.get("git_repository"):
            lines.append(f"<b>Repositório:</b> {escape_html(app.get('git_repository'))}")
        if app.get("git_branch"):
            lines.append(f"<b>Branch:</b> {escape_html(app.get('git_branch'))}")

        buttons = []
        if app.get("fqdn"):
            buttons.append(Button("Abrir aplicação", str(app["fqdn"])))
        await self.telegram.send_message("\n".join(lines), buttons=buttons, chat_id=chat_id)

    async def _deploys(self, chat_id: int, argument: str) -> None:
        deployments = await self.coolify.list_deployments()
        if argument:
            app = await self._find_application(argument)
            if app is None:
                await self._reply(
                    chat_id, f"Aplicação não encontrada: {escape_html(argument)}"
                )
                return
            deployments = [
                deploy
                for deploy in deployments
                if deploy.get("application_uuid") == app.get("uuid")
            ]

        if not deployments:
            await self._reply(chat_id, "Nenhum deploy encontrado.")
            return

        ordered = sorted(
            deployments, key=lambda item: str(item.get("created_at") or ""), reverse=True
        )[:5]
        lines = ["🚀 <b>Últimos deploys</b>\n"]
        for deploy in ordered:
            when = format_brt(deploy.get("created_at"), self.settings.timezone)
            status = escape_html(deploy.get("status") or "?")
            commit = short_commit(deploy.get("commit"))
            name = escape_html(deploy.get("application_name") or "-")
            suffix = f" — <code>{commit}</code>" if commit else ""
            lines.append(f"• {when} — {name} — {status}{suffix}")

        await self._reply(chat_id, "\n".join(lines))

    async def _logs(self, chat_id: int, argument: str) -> None:
        if not argument:
            await self._reply(chat_id, "Uso: /logs &lt;uuid do deploy&gt;")
            return

        deploy = await self.coolify.get_deployment(argument)
        if not deploy:
            await self._reply(chat_id, "Deploy não encontrado.")
            return

        commit = short_commit(deploy.get("commit"))
        lines = [
            f"🧾 <b>Deploy</b> <code>{escape_html(argument)}</code>\n",
            f"<b>Status:</b> {escape_html(deploy.get('status') or 'desconhecido')}",
        ]
        if commit:
            lines.append(f"<b>Commit:</b> <code>{commit}</code>")
        if deploy.get("created_at"):
            lines.append(
                f"<b>Início:</b> {format_brt(deploy.get('created_at'), self.settings.timezone)}"
            )
        if deploy.get("finished_at"):
            lines.append(
                f"<b>Fim:</b> {format_brt(deploy.get('finished_at'), self.settings.timezone)}"
            )
        url = deploy.get("deployment_url")
        if url:
            lines.append(f"<b>Logs:</b> {escape_html(url)}")

        await self._reply(chat_id, "\n".join(lines))

    async def _silence(self, chat_id: int, argument: str) -> None:
        if argument.lower() in {"off", "0", "desligar"}:
            self.store.meta_delete("silent_until")
            await self._reply(chat_id, "🔔 Notificações não críticas reativadas.")
            return

        minutes = _parse_duration(argument)
        if minutes is None:
            await self._reply(chat_id, "Uso: /silenciar &lt;30m|2h|off&gt;")
            return

        until = datetime.now(UTC) + timedelta(minutes=minutes)
        self.store.meta_set("silent_until", until.isoformat())
        until_brt = format_brt(until.isoformat(), self.settings.timezone)
        await self._reply(
            chat_id,
            "🔇 Notificações não críticas silenciadas até "
            f"{until_brt}. As críticas continuam chegando.",
        )

    async def _propose_action(
        self, chat_id: int, user_id: int, action: str, argument: str
    ) -> None:
        if not argument:
            await self._reply(chat_id, f"Uso: /{action} &lt;nome|uuid&gt;")
            return

        app = await self._find_application(argument)
        if app is None:
            await self._reply(
                chat_id, f"Aplicação não encontrada: {escape_html(argument)}"
            )
            return

        app_uuid = str(app.get("uuid") or "")
        app_name = str(app.get("name") or app_uuid)
        label = ACTION_LABEL[action]
        token = uuid.uuid4().hex
        self._pending[token] = PendingAction(
            action=action,
            app_uuid=app_uuid,
            app_name=app_name,
            user_id=user_id,
            chat_id=chat_id,
            expires_at=self._clock() + self.confirm_ttl,
        )

        text = (
            f"❓ <b>Confirmar {label}</b>\n\n"
            f"Aplicação: <b>{escape_html(app_name)}</b>\n"
            f"UUID: <code>{escape_html(app_uuid)}</code>\n\n"
            f"O botão vale por {int(self.confirm_ttl)} s e só pode ser usado uma vez."
        )
        button = Button(
            f"✅ Confirmar {label}",
            callback_data=f"c:{action}:{token}",
        )
        await self._reply(chat_id, text, buttons=[button])

    async def _handle_callback(self, callback: dict) -> None:
        callback_id = str(callback.get("id") or "")
        data = str(callback.get("data") or "")
        user_id = (callback.get("from") or {}).get("id")
        chat_id = ((callback.get("message") or {}).get("chat") or {}).get("id")
        if user_id is None or chat_id is None:
            return

        user_id, chat_id = int(user_id), int(chat_id)
        if not self._authorized(user_id, chat_id):
            LOGGER.warning(
                "Bot: callback negado para user_id=%s chat_id=%s", user_id, chat_id
            )
            await self._answer(callback_id, "Acesso negado.")
            await self._reply(chat_id, DENIED)
            return

        parts = data.split(":")
        if len(parts) != 3 or parts[0] != "c":
            await self._answer(callback_id, "Confirmação inválida.")
            return

        action, token = parts[1], parts[2]
        pending = self._pending.get(token)
        if pending is None:
            await self._answer(callback_id, "Confirmação inválida ou expirada.")
            await self._reply(chat_id, INVALID)
            return

        if pending.user_id != user_id or pending.chat_id != chat_id:
            await self._answer(callback_id, "Esta confirmação não pertence a você.")
            return

        self._pending.pop(token, None)
        if pending.action != action or self._clock() > pending.expires_at:
            await self._answer(callback_id, "Confirmação expirada.")
            await self._reply(chat_id, EXPIRED)
            self.store.audit(user_id, chat_id, action, pending.app_uuid, "expired")
            return

        moment = self._clock()
        last = self._last_action.get(pending.app_uuid)
        if last is not None and moment - last < self.action_rate_limit:
            remaining = int(self.action_rate_limit - (moment - last)) + 1
            await self._answer(callback_id, f"Aguarde {remaining} s.")
            await self._reply(
                chat_id,
                f"⏳ Aguarde {remaining} s antes de outra ação em "
                f"<b>{escape_html(pending.app_name)}</b>.",
            )
            self.store.audit(user_id, chat_id, action, pending.app_uuid, "rate_limited")
            return

        try:
            method = getattr(self.coolify, ACTION_METHOD[action])
            await method(pending.app_uuid)
        except CoolifyError as exc:
            LOGGER.warning("Ação %s falhou: %s", action, exc)
            await self._answer(callback_id, "A ação falhou.")
            await self._reply(
                chat_id,
                f"⚠️ Não foi possível executar {ACTION_LABEL[action]} em "
                f"<b>{escape_html(pending.app_name)}</b>.",
            )
            self.store.audit(user_id, chat_id, action, pending.app_uuid, "error")
            return

        self._last_action[pending.app_uuid] = moment
        self.store.audit(user_id, chat_id, action, pending.app_uuid, "ok")
        await self._answer(callback_id, "Executado.")
        if action == "deploy":
            confirmation = (
                f"✅ <b>Deploy disparado</b> para "
                f"<b>{escape_html(pending.app_name)}</b>.\nAcompanhe em /deploys."
            )
        else:
            confirmation = (
                f"✅ <b>{ACTION_LABEL[action].capitalize()}</b> executado em "
                f"<b>{escape_html(pending.app_name)}</b>."
            )
        await self._reply(chat_id, confirmation)

    async def _answer(self, callback_id: str, text: str) -> None:
        if not callback_id:
            return
        try:
            await self.telegram.answer_callback(callback_id, text)
        except TelegramError as exc:
            LOGGER.warning("Resposta de callback falhou: %s", exc)

    async def _find_application(self, argument: str) -> dict | None:
        applications = await self.coolify.list_applications()
        lowered = argument.lower()
        for app in applications:
            if str(app.get("uuid")) == argument or str(app.get("name", "")).lower() == lowered:
                return app

        if len(argument) >= 8:
            try:
                return await self.coolify.get_application(argument)
            except CoolifyError:
                return None
        return None


def _is_online(server: dict) -> bool:
    value = server.get("is_reachable", server.get("reachable", True))
    if isinstance(value, bool):
        return value
    return str(value).lower() in {"true", "1", "online", "reachable"}

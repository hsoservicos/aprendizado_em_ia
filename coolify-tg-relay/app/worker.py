from __future__ import annotations

import asyncio
import contextlib
import logging
from datetime import UTC, datetime, timedelta
from zoneinfo import ZoneInfo

from app.coolify import CoolifyClient, CoolifyError
from app.format import UnknownEvent, render
from app.store import Store
from app.telegram import TelegramClient, TelegramError
from app.templates import TemplatesConfig

LOGGER = logging.getLogger(__name__)

RETRY_BASE_SECONDS = 30
RETRY_MAX_SECONDS = 900
DEPLOYMENT_EVENTS = frozenset({"deployment_success", "deployment_failed"})

CRITICAL_EVENTS = frozenset(
    {
        "deployment_failed",
        "server_unreachable",
        "restart_limit_reached",
        "high_disk_usage",
    }
)

DIGEST_HOUR = 8
DIGEST_TIMEZONE = "America/Sao_Paulo"


def retry_delay(attempts: int) -> timedelta:
    seconds = min(RETRY_BASE_SECONDS * (2 ** max(0, attempts - 1)), RETRY_MAX_SECONDS)
    return timedelta(seconds=seconds)


def _parse_moment(raw: str | None) -> datetime | None:
    if not raw:
        return None
    try:
        parsed = datetime.fromisoformat(raw)
    except ValueError:
        return None
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=UTC)


class Dispatcher:
    def __init__(
        self,
        store: Store,
        telegram: TelegramClient,
        templates: TemplatesConfig,
        coolify: CoolifyClient | None = None,
        threads: dict[str, int] | None = None,
        timezone: str = DIGEST_TIMEZONE,
        digest_hour: int = DIGEST_HOUR,
    ) -> None:
        self.store = store
        self.telegram = telegram
        self.templates = templates
        self.coolify = coolify
        self.threads = threads or {}
        self.timezone = timezone
        self.digest_hour = digest_hour

    async def dispatch_once(self, now: datetime | None = None) -> int:
        moment = now or datetime.now(UTC)
        silenced_until = self._silenced_until()
        sent = 0

        for item in self.store.claim_due(moment):
            event = str(item.payload.get("event") or "")
            if (
                silenced_until is not None
                and moment < silenced_until
                and event not in CRITICAL_EVENTS
            ):
                LOGGER.info(
                    "Evento %s silenciado até %s",
                    event,
                    silenced_until.isoformat(),
                )
                self.store.mark_sent(item.id)
                continue

            try:
                payload = await self._enrich(item.payload)
                rendered = render(payload, self.templates, now=moment, threads=self.threads)
            except UnknownEvent as exc:
                LOGGER.warning("Evento sem template descartado: %s", exc)
                self.store.mark_sent(item.id)
                continue
            except Exception as exc:  # noqa: BLE001 - falha de enriquecimento não bloqueia envio
                LOGGER.warning("Enriquecimento falhou para %s: %s", item.dedupe_key, exc)
                payload = item.payload
                rendered = render(payload, self.templates, now=moment, threads=self.threads)

            try:
                await self.telegram.send_message(
                    rendered.text, rendered.buttons, rendered.thread_id
                )
            except TelegramError as exc:
                self.store.mark_failed(item.id, str(exc), retry_at=moment + retry_delay(item.attempts))
                LOGGER.warning("Envio falhou (tentativa %s): %s", item.attempts, exc)
                continue

            self.store.mark_sent(item.id)
            self.store.meta_set("last_event", str(payload.get("event") or ""))
            sent += 1

        return sent

    async def maybe_send_digest(self, now: datetime | None = None) -> bool:
        moment = now or datetime.now(UTC)
        local = moment.astimezone(ZoneInfo(self.timezone))
        if local.hour < self.digest_hour:
            return False

        today = local.date().isoformat()
        if self.store.meta_get("last_digest_date") == today:
            return False

        since = _parse_moment(self.store.meta_get("last_digest_at")) or (
            moment - timedelta(days=1)
        )
        stats = {
            event: total
            for event, total in self.store.stats_since(since).items()
            if total
        }
        if not stats:
            return False

        lines = ["🗓️ <b>Resumo diário</b>\n"]
        for event, total in sorted(stats.items()):
            lines.append(f"• {event}: {total}")
        lines.append(f"\n<b>Total:</b> {sum(stats.values())} evento(s)")
        await self.telegram.send_message("\n".join(lines))

        self.store.meta_set("last_digest_at", moment.isoformat())
        self.store.meta_set("last_digest_date", today)
        return True

    def _silenced_until(self) -> datetime | None:
        return _parse_moment(self.store.meta_get("silent_until"))

    async def _enrich(self, payload: dict) -> dict:
        if self.coolify is None:
            return payload

        event = str(payload.get("event") or "")
        uuid = payload.get("deployment_uuid")
        if event not in DEPLOYMENT_EVENTS or not uuid or payload.get("commit"):
            return payload

        try:
            deployment = await self.coolify.get_deployment(str(uuid))
        except CoolifyError as exc:
            LOGGER.warning("Não foi possível enriquecer deploy %s: %s", uuid, exc)
            return payload

        enriched = dict(payload)
        for key in ("commit", "commit_message", "created_at", "finished_at", "status"):
            if not enriched.get(key) and deployment.get(key):
                enriched[key] = deployment[key]
        return enriched


async def run_forever(
    dispatcher: Dispatcher,
    interval: float = 2.0,
    stop_event: asyncio.Event | None = None,
) -> None:
    dispatcher.store.requeue_stale()
    stop_event = stop_event or asyncio.Event()

    while not stop_event.is_set():
        try:
            await dispatcher.dispatch_once()
        except Exception:
            LOGGER.exception("Falha inesperada no dispatcher")
        try:
            await dispatcher.maybe_send_digest()
        except Exception:
            LOGGER.exception("Falha no digest diário")
        with contextlib.suppress(TimeoutError):
            await asyncio.wait_for(stop_event.wait(), timeout=interval)

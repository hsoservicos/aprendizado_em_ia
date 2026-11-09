from app.bot import Bot
from app.config import Settings
from app.store import Store

USER_ID = 42
CHAT_ID = 99


class FakeTelegram:
    def __init__(self, updates: list[dict]) -> None:
        self.updates = updates
        self.sent: list[dict] = []

    async def get_updates(self, offset=None):
        return self.updates

    async def send_message(self, text, buttons=None, thread_id=None, chat_id=None):
        self.sent.append(
            {"text": text, "buttons": buttons, "thread_id": thread_id, "chat_id": chat_id}
        )
        return {"ok": True}

    async def answer_callback(self, callback_id, text):
        return {"ok": True}


class FakeCoolify:
    def __init__(self) -> None:
        self.calls: list[str] = []

    async def list_applications(self):
        self.calls.append("list_applications")
        return [
            {
                "uuid": "app-1",
                "name": "sound-music-app",
                "status": "running:healthy",
                "fqdn": "https://sound.test",
            },
            {"uuid": "app-2", "name": "markdown-studio", "status": "exited"},
        ]

    async def list_servers(self):
        self.calls.append("list_servers")
        return [
            {"uuid": "srv-1", "name": "servitec-local", "is_reachable": True},
            {"uuid": "srv-2", "name": "backup", "is_reachable": False},
        ]

    async def list_deployments(self):
        self.calls.append("list_deployments")
        return []


def _update(text: str, user_id: int = USER_ID, chat_id: int = CHAT_ID) -> dict:
    return {
        "update_id": 1,
        "message": {
            "message_id": 10,
            "from": {"id": user_id},
            "chat": {"id": chat_id},
            "text": text,
        },
    }


def _bot(tmp_path, updates, allowed_users=None, allowed_chats=None):
    settings = Settings(
        allowed_user_ids=allowed_users if allowed_users is not None else {USER_ID},
        allowed_chat_ids=allowed_chats if allowed_chats is not None else {CHAT_ID},
    )
    store = Store(str(tmp_path / "relay.db"))
    telegram = FakeTelegram(updates)
    coolify = FakeCoolify()
    return Bot(telegram, coolify, store, settings), telegram, coolify, store


async def test_denies_unknown_user(tmp_path):
    bot, telegram, coolify, _store = _bot(tmp_path, [_update("/status", user_id=7)])

    await bot.poll_once()

    assert len(telegram.sent) == 1
    assert "Acesso negado" in telegram.sent[0]["text"]
    assert coolify.calls == []


async def test_allows_listed_user_and_chat(tmp_path):
    bot, telegram, coolify, _store = _bot(tmp_path, [_update("/apps")])

    await bot.poll_once()

    assert "list_applications" in coolify.calls
    assert len(telegram.sent) == 1
    assert "sound-music-app" in telegram.sent[0]["text"]
    assert telegram.sent[0]["chat_id"] == CHAT_ID


async def test_status_renders_pt_br(tmp_path):
    bot, telegram, _coolify, _store = _bot(tmp_path, [_update("/status")])

    await bot.poll_once()

    text = telegram.sent[0]["text"]
    assert "Status do Coolify" in text
    assert "Aplicações:" in text
    assert "Servidores:" in text
    assert "Deploys em andamento:" in text

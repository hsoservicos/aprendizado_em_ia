from app.bot import Bot
from app.config import Settings
from app.store import Store

USER_ID = 42
CHAT_ID = 99


class FakeTelegram:
    def __init__(self, updates: list[dict] | None = None) -> None:
        self.updates = updates or []
        self.sent: list[dict] = []
        self.answered: list[tuple[str, str]] = []

    async def get_updates(self, offset=None):
        return self.updates

    async def send_message(self, text, buttons=None, thread_id=None, chat_id=None):
        self.sent.append(
            {
                "text": text,
                "buttons": list(buttons or []),
                "thread_id": thread_id,
                "chat_id": chat_id,
            }
        )
        return {"ok": True}

    async def answer_callback(self, callback_id, text):
        self.answered.append((callback_id, text))
        return {"ok": True}


class FakeCoolify:
    def __init__(self) -> None:
        self.calls: list[tuple[str, str]] = []

    async def list_applications(self):
        return [
            {"uuid": "app-1", "name": "sound-music-app", "status": "running:healthy"},
            {"uuid": "app-2", "name": "markdown-studio", "status": "exited"},
        ]

    async def get_application(self, uuid: str):
        return {"uuid": uuid, "name": uuid, "status": "running"}

    async def deploy(self, uuid: str):
        self.calls.append(("deploy", uuid))
        return {"deployments": [{"deployment_uuid": "dep-1"}]}

    async def start(self, uuid: str):
        self.calls.append(("start", uuid))
        return {}

    async def restart(self, uuid: str):
        self.calls.append(("restart", uuid))
        return {}

    async def stop(self, uuid: str):
        self.calls.append(("stop", uuid))
        return {}


def _message(text: str) -> dict:
    return {
        "update_id": 1,
        "message": {
            "message_id": 10,
            "from": {"id": USER_ID},
            "chat": {"id": CHAT_ID},
            "text": text,
        },
    }


def _callback(data: str, user_id: int = USER_ID, chat_id: int = CHAT_ID) -> dict:
    return {
        "update_id": 2,
        "callback_query": {
            "id": "cb-1",
            "from": {"id": user_id},
            "data": data,
            "message": {"message_id": 11, "chat": {"id": chat_id}},
        },
    }


class Clock:
    def __init__(self, value: float = 1000.0) -> None:
        self.value = value

    def __call__(self) -> float:
        return self.value

    def advance(self, seconds: float) -> None:
        self.value += seconds


def _bot(tmp_path):
    settings = Settings(allowed_user_ids={USER_ID}, allowed_chat_ids={CHAT_ID})
    store = Store(str(tmp_path / "relay.db"))
    telegram = FakeTelegram()
    coolify = FakeCoolify()
    clock = Clock()
    bot = Bot(telegram, coolify, store, settings, clock=clock)
    return bot, telegram, coolify, store, clock


async def _propose(bot, telegram, command: str) -> str:
    await bot.handle_update(_message(command))
    buttons = [b for b in telegram.sent[-1]["buttons"] if getattr(b, "callback_data", None)]
    assert buttons, "a confirmação deve oferecer um botão com callback_data"
    return buttons[0].callback_data


def _texts(telegram) -> str:
    return "\n".join(item["text"] for item in telegram.sent)


async def test_action_requires_confirmation(tmp_path):
    bot, telegram, coolify, _store, _clock = _bot(tmp_path)

    data = await _propose(bot, telegram, "/deploy sound-music-app")

    assert coolify.calls == []
    assert data.startswith("c:deploy:")
    assert "Confirmar" in telegram.sent[-1]["text"]


async def test_confirmation_expires_after_60s(tmp_path):
    bot, telegram, coolify, _store, clock = _bot(tmp_path)
    data = await _propose(bot, telegram, "/parar sound-music-app")

    clock.advance(61)
    await bot.handle_update(_callback(data))

    assert coolify.calls == []
    assert "expir" in _texts(telegram).lower()


async def test_callback_is_single_use(tmp_path):
    bot, telegram, coolify, _store, _clock = _bot(tmp_path)
    data = await _propose(bot, telegram, "/reiniciar sound-music-app")

    await bot.handle_update(_callback(data))
    await bot.handle_update(_callback(data))

    assert coolify.calls == [("restart", "app-1")]
    assert "expirada" in _texts(telegram).lower() or "inválida" in _texts(telegram).lower()


async def test_rate_limits_actions_per_app(tmp_path):
    bot, telegram, coolify, _store, clock = _bot(tmp_path)
    first = await _propose(bot, telegram, "/deploy sound-music-app")
    second = await _propose(bot, telegram, "/deploy sound-music-app")

    await bot.handle_update(_callback(first))
    clock.advance(5)
    await bot.handle_update(_callback(second))

    assert coolify.calls == [("deploy", "app-1")]
    assert "Aguarde" in _texts(telegram)


async def test_audit_written_for_action(tmp_path):
    bot, telegram, coolify, store, _clock = _bot(tmp_path)
    data = await _propose(bot, telegram, "/iniciar sound-music-app")

    await bot.handle_update(_callback(data))

    assert coolify.calls == [("start", "app-1")]
    rows = store.audit_rows()
    assert len(rows) == 1
    row = rows[0]
    assert row["action"] == "iniciar"
    assert row["target"] == "app-1"
    assert row["result"] == "ok"
    assert row["user_id"] == USER_ID
    assert row["chat_id"] == CHAT_ID

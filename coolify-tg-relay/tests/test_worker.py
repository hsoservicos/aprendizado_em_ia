from datetime import UTC, datetime, timedelta

from app.store import Store
from app.telegram import TelegramError
from app.templates import load_templates
from app.worker import Dispatcher

NOW = datetime(2026, 11, 9, 12, 0, tzinfo=UTC)
TEMPLATES = load_templates()

PAYLOAD = {
    "event": "deployment_success",
    "deployment_uuid": "dep-1",
    "application_name": "sound-music-app",
    "project": "Serviços",
    "environment": "production",
    "commit": "bb24bb9185a7470f18900e9a0835fc9b14966db1",
    "created_at": "2026-11-08T03:22:09Z",
    "finished_at": "2026-11-08T03:24:53Z",
}


class FakeTelegram:
    def __init__(self, fail: bool = False) -> None:
        self.fail = fail
        self.calls: list[dict] = []

    async def send_message(self, text, buttons=None, thread_id=None):
        self.calls.append({"text": text, "buttons": buttons, "thread_id": thread_id})
        if self.fail:
            raise TelegramError("Telegram respondeu 502")
        return {"ok": True, "result": {"message_id": len(self.calls)}}


def _store(tmp_path) -> Store:
    store = Store(str(tmp_path / "relay.db"))
    store.enqueue("deployment_success:dep-1:", PAYLOAD, now=NOW)
    return store


async def test_dispatcher_sends_and_marks_sent(tmp_path):
    store = _store(tmp_path)
    telegram = FakeTelegram()
    dispatcher = Dispatcher(store, telegram, TEMPLATES)

    sent = await dispatcher.dispatch_once(NOW)

    assert sent == 1
    assert len(telegram.calls) == 1
    assert telegram.calls[0]["text"].startswith("✅ <b>Deploy concluído</b>")
    assert store.pending_count() == 0
    assert store.meta_get("last_event") == "deployment_success"


async def test_dispatcher_retries_on_5xx(tmp_path):
    store = _store(tmp_path)
    telegram = FakeTelegram(fail=True)
    dispatcher = Dispatcher(store, telegram, TEMPLATES)

    assert await dispatcher.dispatch_once(NOW) == 0
    assert len(telegram.calls) == 1
    assert store.pending_count() == 1

    assert await dispatcher.dispatch_once(NOW) == 0
    assert len(telegram.calls) == 1

    assert await dispatcher.dispatch_once(NOW + timedelta(minutes=10)) == 0
    assert len(telegram.calls) == 2

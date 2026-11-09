from datetime import UTC, datetime, timedelta

from app.store import Store
from app.templates import load_templates
from app.worker import Dispatcher


class FakeTelegram:
    def __init__(self) -> None:
        self.sent: list[str] = []

    async def send_message(self, text, buttons=None, thread_id=None, chat_id=None):
        self.sent.append(text)
        return {"ok": True}


def _event(name: str, uuid: str, status: str = "finished") -> dict:
    return {
        "event": name,
        "application_name": "sound-music-app",
        "deployment_uuid": uuid,
        "status": status,
    }


async def test_silence_skips_non_critical_events(tmp_path):
    store = Store(str(tmp_path / "relay.db"))
    telegram = FakeTelegram()
    dispatcher = Dispatcher(store, telegram, load_templates())
    now = datetime(2026, 11, 9, 14, 0, tzinfo=UTC)

    store.meta_set("silent_until", (now + timedelta(minutes=30)).isoformat())
    store.enqueue(
        "deployment_success:d1",
        _event("deployment_success", "d1"),
        now=now,
    )
    store.enqueue(
        "deployment_failed:d2",
        _event("deployment_failed", "d2", status="failed"),
        now=now,
    )

    sent = await dispatcher.dispatch_once(now)

    assert sent == 1
    assert len(telegram.sent) == 1
    assert "Falha" in telegram.sent[0]
    assert store.pending_count() == 0


async def test_digest_aggregates_counts(tmp_path):
    store = Store(str(tmp_path / "relay.db"))
    telegram = FakeTelegram()
    dispatcher = Dispatcher(store, telegram, load_templates())
    now = datetime(2026, 11, 9, 11, 0, tzinfo=UTC)  # 08:00 em America/Sao_Paulo
    earlier = now - timedelta(hours=1)

    for index in range(2):
        store.enqueue(
            f"deployment_success:d{index}",
            _event("deployment_success", f"d{index}"),
            now=earlier,
        )
    store.enqueue(
        "task_failed:t1",
        {
            "event": "task_failed",
            "task_name": "backup",
            "application_name": "sound-music-app",
            "task_uuid": "t1",
            "status": "failed",
        },
        now=earlier,
    )

    assert await dispatcher.maybe_send_digest(now) is True
    text = telegram.sent[-1]
    assert "Resumo diário" in text
    assert "deployment_success: 2" in text
    assert "task_failed: 1" in text

    assert await dispatcher.maybe_send_digest(now + timedelta(minutes=10)) is False
    assert len(telegram.sent) == 1

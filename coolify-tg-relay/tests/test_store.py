from datetime import UTC, datetime, timedelta

from app.store import Store, build_dedupe_key


def _now() -> datetime:
    return datetime(2026, 11, 9, 12, 0, tzinfo=UTC)


def test_enqueue_dedupes_same_key(tmp_path):
    store = Store(str(tmp_path / "relay.db"))

    first = store.enqueue("deployment_success:abc:", {"event": "deployment_success"})
    second = store.enqueue("deployment_success:abc:", {"event": "deployment_success"})

    assert first is not None
    assert second is None
    assert store.pending_count() == 1


def test_claim_due_only_returns_due_items(tmp_path):
    store = Store(str(tmp_path / "relay.db"))
    store.enqueue("a", {"event": "deployment_success"}, now=_now())
    store.enqueue("b", {"event": "deployment_failed"}, now=_now())

    claimed = store.claim_due(_now())
    assert [item.dedupe_key for item in claimed] == ["a", "b"]

    store.mark_sent(claimed[0].id)
    store.mark_failed(claimed[1].id, "erro", retry_at=_now() + timedelta(minutes=5))

    assert store.claim_due(_now()) == []
    retried = store.claim_due(_now() + timedelta(minutes=6))
    assert [item.dedupe_key for item in retried] == ["b"]
    assert retried[0].attempts == 2


def test_mark_failed_schedules_retry(tmp_path):
    store = Store(str(tmp_path / "relay.db"))
    item_id = store.enqueue("c", {"event": "task_failed"}, now=_now())
    item = store.claim_due(_now())[0]
    retry_at = _now() + timedelta(minutes=10)

    store.mark_failed(item.id, "telegram 500", retry_at=retry_at)

    due_now = store.claim_due(_now())
    assert due_now == []
    later = store.claim_due(retry_at)
    assert len(later) == 1
    assert later[0].id == item_id
    assert later[0].last_error == "telegram 500"


def test_audit_persists_rows(tmp_path):
    store = Store(str(tmp_path / "relay.db"))

    store.audit(42, 99, "deploy", "sound-music-app", "ok")

    rows = store.audit_rows()
    assert len(rows) == 1
    assert rows[0]["user_id"] == 42
    assert rows[0]["chat_id"] == 99
    assert rows[0]["action"] == "deploy"
    assert rows[0]["target"] == "sound-music-app"
    assert rows[0]["result"] == "ok"


def test_meta_and_stats(tmp_path):
    store = Store(str(tmp_path / "relay.db"))

    store.meta_set("last_event", "deployment_success")
    assert store.meta_get("last_event") == "deployment_success"
    assert store.meta_get("nao_existe") is None

    store.enqueue("d", {"event": "deployment_success"}, now=_now())
    store.enqueue("e", {"event": "task_failed"}, now=_now())

    stats = store.stats_since(_now() - timedelta(hours=1))
    assert stats == {"deployment_success": 1, "task_failed": 1}


def test_build_dedupe_key_uses_ids_and_minute_bucket():
    payload = {"event": "deployment_success", "deployment_uuid": "dep-1"}

    assert build_dedupe_key(payload, _now()) == "deployment_success:dep-1:"

    disk = {"event": "high_disk_usage", "server_uuid": "srv-1"}
    first = build_dedupe_key(disk, _now())
    second = build_dedupe_key(disk, _now() + timedelta(minutes=1))
    assert first != second

from __future__ import annotations

import hashlib
import json
import sqlite3
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from pathlib import Path

REPEATING_EVENTS = frozenset(
    {
        "high_disk_usage",
        "server_unreachable",
        "server_reachable",
        "docker_cleanup_success",
        "docker_cleanup_failed",
        "traefik_version_outdated",
    }
)

IDENTIFIER_FIELDS = (
    "deployment_uuid",
    "task_uuid",
    "database_uuid",
    "server_uuid",
    "container_name",
)

SCHEMA = """
CREATE TABLE IF NOT EXISTS outbox (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dedupe_key TEXT NOT NULL UNIQUE,
    payload TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending',
    attempts INTEGER NOT NULL DEFAULT 0,
    next_at TEXT NOT NULL,
    last_error TEXT,
    created_at TEXT NOT NULL,
    claimed_at TEXT
);

CREATE INDEX IF NOT EXISTS idx_outbox_due ON outbox (status, next_at);

CREATE TABLE IF NOT EXISTS audit (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ts TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    chat_id INTEGER NOT NULL,
    action TEXT NOT NULL,
    target TEXT NOT NULL,
    result TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS meta (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);
"""


@dataclass(frozen=True)
class OutboxItem:
    id: int
    dedupe_key: str
    payload: dict
    status: str
    attempts: int
    last_error: str | None


def _iso(value: datetime | None = None) -> str:
    value = value or datetime.now(UTC)
    if value.tzinfo is None:
        value = value.replace(tzinfo=UTC)
    return value.astimezone(UTC).isoformat()


def build_dedupe_key(payload: dict, now: datetime | None = None) -> str:
    event = str(payload.get("event") or "unknown")

    identifier = ""
    for field in IDENTIFIER_FIELDS:
        value = payload.get(field)
        if value:
            identifier = str(value)
            break

    if not identifier:
        digest = hashlib.sha1(
            json.dumps(payload, sort_keys=True, default=str).encode("utf-8")
        ).hexdigest()
        identifier = digest[:12]

    bucket = ""
    if event in REPEATING_EVENTS:
        bucket = _iso(now)[:16].replace("-", "").replace(":", "").replace("T", "")

    return f"{event}:{identifier}:{bucket}"


class Store:
    def __init__(self, path: str) -> None:
        self.path = path
        if path != ":memory:":
            Path(path).parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as conn:
            conn.executescript(SCHEMA)

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.path, timeout=10)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA busy_timeout=5000")
        return conn

    def enqueue(
        self, dedupe_key: str, payload: dict, now: datetime | None = None
    ) -> int | None:
        created_at = _iso(now)
        with self._connect() as conn:
            cursor = conn.execute(
                """
                INSERT OR IGNORE INTO outbox
                    (dedupe_key, payload, status, attempts, next_at, created_at)
                VALUES (?, ?, 'pending', 0, ?, ?)
                """,
                (dedupe_key, json.dumps(payload, ensure_ascii=False), created_at, created_at),
            )
            return cursor.lastrowid if cursor.rowcount else None

    def claim_due(self, now: datetime | None = None) -> list[OutboxItem]:
        moment = _iso(now)
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT id, dedupe_key, payload, status, attempts, last_error
                FROM outbox
                WHERE status = 'pending' AND next_at <= ?
                ORDER BY id
                """,
                (moment,),
            ).fetchall()

            for row in rows:
                conn.execute(
                    """
                    UPDATE outbox
                    SET status = 'processing', attempts = attempts + 1, claimed_at = ?
                    WHERE id = ?
                    """,
                    (moment, row["id"]),
                )

        return [
            OutboxItem(
                id=row["id"],
                dedupe_key=row["dedupe_key"],
                payload=json.loads(row["payload"]),
                status="processing",
                attempts=row["attempts"] + 1,
                last_error=row["last_error"],
            )
            for row in rows
        ]

    def mark_sent(self, item_id: int) -> None:
        with self._connect() as conn:
            conn.execute(
                "UPDATE outbox SET status = 'sent', claimed_at = NULL WHERE id = ?",
                (item_id,),
            )

    def mark_failed(self, item_id: int, error: str, retry_at: datetime | None = None) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                UPDATE outbox
                SET status = 'pending', claimed_at = NULL, next_at = ?, last_error = ?
                WHERE id = ?
                """,
                (_iso(retry_at or datetime.now(UTC) + timedelta(minutes=1)), error, item_id),
            )

    def requeue_stale(
        self, now: datetime | None = None, older_than: timedelta = timedelta(minutes=5)
    ) -> int:
        cutoff = _iso((now or datetime.now(UTC)) - older_than)
        with self._connect() as conn:
            cursor = conn.execute(
                """
                UPDATE outbox
                SET status = 'pending', claimed_at = NULL
                WHERE status = 'processing' AND claimed_at <= ?
                """,
                (cutoff,),
            )
            return cursor.rowcount

    def pending_count(self) -> int:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT COUNT(*) AS total FROM outbox WHERE status IN ('pending', 'processing')"
            ).fetchone()
        return int(row["total"])

    def audit(self, user_id: int, chat_id: int, action: str, target: str, result: str) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO audit (ts, user_id, chat_id, action, target, result)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (_iso(), user_id, chat_id, action, target, result),
            )

    def audit_rows(self) -> list[sqlite3.Row]:
        with self._connect() as conn:
            return conn.execute("SELECT * FROM audit ORDER BY id").fetchall()

    def meta_set(self, key: str, value: str) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO meta (key, value) VALUES (?, ?)
                ON CONFLICT(key) DO UPDATE SET value = excluded.value
                """,
                (key, value),
            )

    def meta_get(self, key: str) -> str | None:
        with self._connect() as conn:
            row = conn.execute("SELECT value FROM meta WHERE key = ?", (key,)).fetchone()
        return row["value"] if row else None

    def meta_delete(self, key: str) -> None:
        with self._connect() as conn:
            conn.execute("DELETE FROM meta WHERE key = ?", (key,))

    def stats_since(self, since: datetime) -> dict[str, int]:
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT json_extract(payload, '$.event') AS event, COUNT(*) AS total
                FROM outbox
                WHERE created_at >= ?
                GROUP BY event
                """,
                (_iso(since),),
            ).fetchall()
        return {row["event"] or "unknown": int(row["total"]) for row in rows}

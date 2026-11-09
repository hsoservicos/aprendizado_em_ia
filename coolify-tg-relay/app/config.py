from __future__ import annotations

import json
import os
from collections.abc import Mapping

from pydantic import BaseModel, Field

REQUIRED_FIELDS = (
    "telegram_bot_token",
    "telegram_chat_id",
    "hook_secret",
    "coolify_api_token",
)

MIN_HOOK_SECRET_LENGTH = 32


class Settings(BaseModel):
    telegram_bot_token: str = ""
    telegram_chat_id: str = ""
    telegram_threads: dict[str, int] = Field(default_factory=dict)
    allowed_user_ids: set[int] = Field(default_factory=set)
    allowed_chat_ids: set[int] = Field(default_factory=set)
    hook_secret: str = ""
    coolify_base_url: str = "http://coolify:8080"
    coolify_api_token: str = ""
    database_path: str = "/data/relay.db"
    timezone: str = "America/Sao_Paulo"
    quiet_hours: tuple[int, int] | None = None
    log_level: str = "INFO"


def _parse_int_set(raw: str | None) -> set[int]:
    if not raw:
        return set()
    values = set()
    for part in raw.replace(";", ",").split(","):
        part = part.strip()
        if not part:
            continue
        values.add(int(part))
    return values


def _parse_threads(raw: str | None) -> dict[str, int]:
    if not raw:
        return {}
    data = json.loads(raw)
    return {str(key): int(value) for key, value in data.items()}


def _parse_quiet_hours(raw: str | None) -> tuple[int, int] | None:
    if not raw:
        return None
    start, end = raw.split("-", 1)
    start_hour, end_hour = int(start), int(end)
    if not (0 <= start_hour <= 23 and 0 <= end_hour <= 23):
        raise ValueError("QUIET_HOURS deve usar horas entre 0 e 23, no formato '23-6'.")
    return start_hour, end_hour


def load_settings(env: Mapping[str, str] | None = None) -> Settings:
    source = os.environ if env is None else env

    values = {
        "telegram_bot_token": source.get("TELEGRAM_BOT_TOKEN", "").strip(),
        "telegram_chat_id": source.get("TELEGRAM_CHAT_ID", "").strip(),
        "telegram_threads": _parse_threads(source.get("TELEGRAM_THREADS")),
        "allowed_user_ids": _parse_int_set(source.get("TELEGRAM_ALLOWED_USER_IDS")),
        "allowed_chat_ids": _parse_int_set(source.get("TELEGRAM_ALLOWED_CHAT_IDS")),
        "hook_secret": source.get("HOOK_SECRET", "").strip(),
        "coolify_base_url": source.get("COOLIFY_BASE_URL", "http://coolify:8080").rstrip("/"),
        "coolify_api_token": source.get("COOLIFY_API_TOKEN", "").strip(),
        "database_path": source.get("DATABASE_PATH", "/data/relay.db"),
        "timezone": source.get("TZ", "America/Sao_Paulo"),
        "quiet_hours": _parse_quiet_hours(source.get("QUIET_HOURS")),
        "log_level": source.get("LOG_LEVEL", "INFO").upper(),
    }

    missing = [name for name in REQUIRED_FIELDS if not values[name]]
    if missing:
        names = ", ".join(name.upper() for name in missing)
        raise RuntimeError(f"Variáveis de ambiente obrigatórias ausentes: {names}")

    if len(values["hook_secret"]) < MIN_HOOK_SECRET_LENGTH:
        raise RuntimeError(
            f"HOOK_SECRET deve ter pelo menos {MIN_HOOK_SECRET_LENGTH} caracteres."
        )

    return Settings(**values)

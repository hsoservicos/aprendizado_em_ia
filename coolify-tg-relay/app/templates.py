from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml

DEFAULT_TEMPLATES_PATH = Path(__file__).with_name("templates.yml")

EVENT_IDS: tuple[str, ...] = (
    "deployment_success",
    "deployment_failed",
    "status_changed",
    "container_restarted",
    "restart_limit_reached",
    "backup_success",
    "backup_failed",
    "backup_success_with_s3_warning",
    "task_success",
    "task_failed",
    "docker_cleanup_success",
    "docker_cleanup_failed",
    "server_reachable",
    "server_unreachable",
    "high_disk_usage",
    "server_patch_check",
    "server_patch_check_error",
    "traefik_version_outdated",
    "test",
)

EVENT_ALIASES: dict[str, str] = {
    "container_stopped": "status_changed",
}


@dataclass(frozen=True)
class Button:
    text: str
    url: str = ""
    callback_data: str | None = None


@dataclass(frozen=True)
class EventTemplate:
    title: str
    body: list[str]
    buttons: list[Button]


@dataclass(frozen=True)
class TemplatesConfig:
    events: dict[str, EventTemplate]


def load_templates(path: str | Path = DEFAULT_TEMPLATES_PATH) -> TemplatesConfig:
    raw = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    raw_events = raw.get("events") or {}

    missing = [event for event in EVENT_IDS if event not in raw_events]
    if missing:
        raise ValueError(f"Templates ausentes: {', '.join(missing)}")

    events = {
        name: EventTemplate(
            title=str(data["title"]),
            body=[str(line) for line in (data.get("body") or [])],
            buttons=[Button(text=str(item["text"]), url=str(item["url"])) for item in (data.get("buttons") or [])],
        )
        for name, data in raw_events.items()
    }

    return TemplatesConfig(events=events)

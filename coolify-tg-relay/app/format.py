from __future__ import annotations

import html
import re
from dataclasses import dataclass
from datetime import UTC, datetime
from zoneinfo import ZoneInfo

from app.templates import EVENT_ALIASES, Button, TemplatesConfig

PLACEHOLDER = re.compile(r"\{([a-zA-Z_][a-zA-Z0-9_]*)\}")
MAX_MESSAGE = 4096
DEFAULT_TIMEZONE = "America/Sao_Paulo"
TRUNCATED_SUFFIX = "\n…(mensagem truncada)"


class UnknownEvent(Exception):
    """Evento sem template configurado."""


@dataclass(frozen=True)
class Rendered:
    text: str
    buttons: list[Button]
    thread_id: int | None


class _MissingField(Exception):
    pass


def escape_html(value: object) -> str:
    return html.escape(str(value), quote=False)


def _parse_datetime(value: object) -> datetime | None:
    if isinstance(value, datetime):
        return value if value.tzinfo else value.replace(tzinfo=UTC)
    if not value:
        return None
    text = str(value).strip().replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        return None
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=UTC)


def format_brt(value: object, timezone: str = DEFAULT_TIMEZONE) -> str:
    parsed = _parse_datetime(value)
    if parsed is None:
        return ""
    return parsed.astimezone(ZoneInfo(timezone)).strftime("%d/%m/%Y %H:%M")


def human_duration(start: object, end: object) -> str:
    begin = _parse_datetime(start)
    finish = _parse_datetime(end)
    if begin is None or finish is None:
        return ""

    seconds = max(0, int((finish - begin).total_seconds()))
    if seconds < 60:
        return f"{seconds} s"
    minutes, rest = divmod(seconds, 60)
    if minutes < 60:
        return f"{minutes} min {rest} s"
    hours, minutes = divmod(minutes, 60)
    return f"{hours} h {minutes} min"


def short_commit(value: object) -> str:
    return str(value)[:8] if value else ""


def truncate(
    text: str, limit: int = MAX_MESSAGE, suffix: str = TRUNCATED_SUFFIX
) -> str:
    if len(text) <= limit:
        return text
    cut = text.rfind("\n", 0, limit - len(suffix))
    if cut < 0:
        cut = limit - len(suffix)
    return text[:cut].rstrip() + suffix


def _inline(value: object, limit: int) -> str:
    if value is None:
        return ""
    text = str(value).strip()
    if len(text) <= limit:
        return text
    return text[:limit].rstrip() + "…"


def _resolve(line: str, context: dict, escape: bool = True) -> str | None:
    def replace(match: re.Match[str]) -> str:
        value = context.get(match.group(1))
        if value is None or value == "":
            raise _MissingField
        return escape_html(value) if escape else str(value)

    try:
        return PLACEHOLDER.sub(replace, line)
    except _MissingField:
        return None


def _build_context(payload: dict, extra: dict | None, now: datetime | None) -> dict:
    context = dict(payload)
    context.update(extra or {})

    moment = now or datetime.now(UTC)
    context["now_brt"] = format_brt(moment)
    context["resource_label"] = next(
        (
            str(context[field])
            for field in ("resource_name", "application_name", "container_name", "database_name")
            if context.get(field)
        ),
        "",
    )
    context["commit_short"] = short_commit(context.get("commit"))
    context["duration"] = human_duration(context.get("created_at"), context.get("finished_at"))
    context["finished_at_brt"] = format_brt(
        context.get("finished_at") or context.get("created_at")
    )
    context["error_short"] = _inline(
        context.get("error_output")
        or context.get("error_message")
        or context.get("error"),
        600,
    )
    context["s3_error_short"] = _inline(context.get("s3_error"), 400)
    context["cleanup_short"] = _inline(context.get("cleanup_message"), 400)
    context["task_output_short"] = _inline(context.get("output"), 800)

    servers = context.get("servers") or []
    if servers:
        first = servers[0]
        context.setdefault("server_name", first.get("name"))
        context["current_version"] = first.get("current_version")
        context["latest_version"] = first.get("latest_version")

    return context


def render(
    payload: dict,
    config: TemplatesConfig,
    extra: dict | None = None,
    now: datetime | None = None,
    threads: dict[str, int] | None = None,
) -> Rendered:
    event = str(payload.get("event") or "")
    template_name = event if event in config.events else EVENT_ALIASES.get(event, event)
    template = config.events.get(template_name)
    if template is None:
        raise UnknownEvent(event)

    context = _build_context(payload, extra, now)

    lines = []
    for line in template.body:
        rendered_line = _resolve(line, context)
        if rendered_line is not None:
            lines.append(rendered_line)

    text = template.title if not lines else f"{template.title}\n\n" + "\n".join(lines)
    text = truncate(text)

    buttons: list[Button] = []
    seen_urls: set[str] = set()
    for button in template.buttons:
        url = _resolve(button.url, context, escape=False)
        if not url or not url.startswith("http") or url in seen_urls:
            continue
        seen_urls.add(url)
        buttons.append(Button(text=button.text, url=url))

    thread_id = None
    if threads:
        thread_id = threads.get(event) or threads.get(template_name)

    return Rendered(text=text, buttons=buttons, thread_id=thread_id)

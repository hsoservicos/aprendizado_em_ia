import json
from datetime import UTC, datetime
from pathlib import Path

import pytest

from app.format import render
from app.templates import DEFAULT_TEMPLATES_PATH, EVENT_IDS, load_templates

NOW = datetime(2026, 11, 9, 11, 30, tzinfo=UTC)
ROOT = Path(__file__).parent
FIXTURES = ROOT / "fixtures" / "payloads"
GOLDEN = ROOT / "golden"


@pytest.fixture(scope="module")
def cfg():
    return load_templates(str(DEFAULT_TEMPLATES_PATH))


def _payload(event: str) -> dict:
    return json.loads((FIXTURES / f"{event}.json").read_text(encoding="utf-8"))


def _golden(event: str) -> str:
    return (GOLDEN / f"{event}.txt").read_text(encoding="utf-8").rstrip("\n")


@pytest.mark.parametrize("event", EVENT_IDS)
def test_golden_message(cfg, event):
    out = render(_payload(event), cfg, now=NOW)

    assert out.text == _golden(event)


@pytest.mark.parametrize("event", EVENT_IDS)
def test_no_unresolved_or_empty_placeholders(cfg, event):
    out = render(_payload(event), cfg, now=NOW)

    assert "{" not in out.text
    assert "}" not in out.text
    assert "None" not in out.text


def test_every_event_has_template(cfg):
    assert set(EVENT_IDS) == set(cfg.events)


def test_container_stopped_uses_status_changed_template(cfg):
    payload = _payload("status_changed")
    payload["event"] = "container_stopped"

    out = render(payload, cfg, now=NOW)

    assert out.text == _golden("status_changed")

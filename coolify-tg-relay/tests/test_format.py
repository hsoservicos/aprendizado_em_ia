from datetime import UTC, datetime

from app.format import (
    Button,
    escape_html,
    format_brt,
    human_duration,
    render,
    short_commit,
    truncate,
)
from app.templates import EventTemplate, TemplatesConfig

NOW = datetime(2026, 11, 9, 11, 30, tzinfo=UTC)


def test_escape_html():
    assert escape_html("a & b < c > d") == "a &amp; b &lt; c &gt; d"


def test_format_brt():
    assert format_brt("2026-11-08T03:24:53Z") == "08/11/2026 00:24"
    assert format_brt(None) == ""


def test_human_duration():
    assert human_duration("2026-11-08T03:22:09Z", "2026-11-08T03:24:53Z") == "2 min 44 s"
    assert human_duration(None, None) == ""


def test_short_commit():
    assert short_commit("bb24bb9185a7470f18900e9a0835fc9b14966db1") == "bb24bb91"
    assert short_commit(None) == ""


def test_truncate():
    out = truncate("x" * 5000)

    assert len(out) <= 4096
    assert out.endswith("…(mensagem truncada)")


def test_render_drops_line_with_missing_field():
    cfg = TemplatesConfig(
        events={"e": EventTemplate(title="T", body=["a {x}", "b {y}"], buttons=[])}
    )

    out = render({"event": "e", "y": "ok"}, cfg, now=NOW)

    assert out.text == "T\n\nb ok"


def test_render_drops_button_without_http():
    cfg = TemplatesConfig(
        events={
            "e": EventTemplate(
                title="T",
                body=[],
                buttons=[Button("sem url", "{fqdn}"), Button("ok", "https://x.test")],
            )
        }
    )

    out = render({"event": "e"}, cfg, now=NOW)

    assert out.buttons == [Button("ok", "https://x.test")]


def test_render_sets_thread_from_map():
    cfg = TemplatesConfig(events={"e": EventTemplate(title="T", body=[], buttons=[])})

    out = render({"event": "e"}, cfg, now=NOW, threads={"e": 12})

    assert out.thread_id == 12


def test_render_escapes_values():
    cfg = TemplatesConfig(
        events={"e": EventTemplate(title="T", body=["<b>{name}</b>"], buttons=[])}
    )

    out = render({"event": "e", "name": "a < b & c"}, cfg, now=NOW)

    assert out.text == "T\n\n<b>a &lt; b &amp; c</b>"

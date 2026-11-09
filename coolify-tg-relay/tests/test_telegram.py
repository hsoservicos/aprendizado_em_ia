import json

import httpx
import pytest

from app.format import Button
from app.telegram import TelegramClient, TelegramError

TOKEN = "123456:test-token"
CHAT_ID = "987654321"


class FakeSleep:
    def __init__(self) -> None:
        self.delays: list[float] = []

    async def __call__(self, delay: float) -> None:
        self.delays.append(delay)


def _client(responses, sleep=None):
    requests: list[httpx.Request] = []

    async def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return responses.pop(0)

    http = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    return TelegramClient(TOKEN, CHAT_ID, http, sleep=sleep or FakeSleep()), requests, http


async def test_send_message_uses_html_and_thread():
    client, requests, http = _client([httpx.Response(200, json={"ok": True})])
    async with http:
        await client.send_message(
            "✅ <b>Deploy concluído</b>",
            [Button("Abrir aplicação", "https://sound.test")],
            thread_id=12,
        )

    payload = json.loads(requests[0].content)
    assert str(requests[0].url) == f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    assert payload["chat_id"] == CHAT_ID
    assert payload["parse_mode"] == "HTML"
    assert payload["disable_web_page_preview"] is True
    assert payload["message_thread_id"] == 12
    keyboard = json.loads(payload["reply_markup"])["inline_keyboard"]
    assert keyboard == [[{"text": "Abrir aplicação", "url": "https://sound.test"}]]


async def test_retry_after_429():
    sleep = FakeSleep()
    client, requests, http = _client(
        [
            httpx.Response(429, json={"ok": False, "parameters": {"retry_after": 3}}),
            httpx.Response(200, json={"ok": True}),
        ],
        sleep=sleep,
    )

    async with http:
        await client.send_message("oi")

    assert sleep.delays == [3]
    assert len(requests) == 2


async def test_fallback_when_button_url_rejected():
    client, requests, http = _client(
        [
            httpx.Response(400, json={"ok": False, "description": "Bad Request: BUTTON_URL_INVALID"}),
            httpx.Response(200, json={"ok": True}),
        ]
    )

    async with http:
        await client.send_message(
            "✅ Deploy concluído", [Button("Abrir aplicação", "https://sound.test")]
        )

    retry_payload = json.loads(requests[1].content)
    assert "reply_markup" not in retry_payload
    assert "Abrir aplicação: https://sound.test" in retry_payload["text"]


async def test_truncates_before_send():
    client, requests, http = _client([httpx.Response(200, json={"ok": True})])

    async with http:
        await client.send_message("x" * 5000)

    payload = json.loads(requests[0].content)
    assert len(payload["text"]) <= 4096
    assert payload["text"].endswith("…(mensagem truncada)")


async def test_server_error_raises():
    client, _requests, http = _client([httpx.Response(502, json={"ok": False})])

    async with http:
        with pytest.raises(TelegramError):
            await client.send_message("oi")


async def test_get_updates_and_answer_callback():
    client, requests, http = _client(
        [
            httpx.Response(200, json={"ok": True, "result": [{"update_id": 1}]}),
            httpx.Response(200, json={"ok": True}),
        ]
    )

    async with http:
        updates = await client.get_updates(offset=5)
        await client.answer_callback("cb-1", "Ação confirmada")

    assert updates == [{"update_id": 1}]
    assert "offset=5" in str(requests[0].url)
    assert "getUpdates" in str(requests[0].url)
    assert json.loads(requests[1].content) == {
        "callback_query_id": "cb-1",
        "text": "Ação confirmada",
    }

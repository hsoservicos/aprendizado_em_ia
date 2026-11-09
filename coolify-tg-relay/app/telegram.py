from __future__ import annotations

import asyncio
import json
from collections.abc import Awaitable, Callable

import httpx

from app.format import Button, truncate

API_BASE = "https://api.telegram.org"

MAX_ATTEMPTS = 2


class TelegramError(RuntimeError):
    """Falha ao conversar com a API do Telegram."""


class TelegramClient:
    def __init__(
        self,
        token: str,
        chat_id: str,
        http: httpx.AsyncClient,
        sleep: Callable[[float], Awaitable[None]] | None = None,
    ) -> None:
        self.token = token
        self.chat_id = chat_id
        self.http = http
        self._sleep = sleep or asyncio.sleep

    def _url(self, method: str) -> str:
        return f"{API_BASE}/bot{self.token}/{method}"

    async def _post(self, method: str, payload: dict) -> dict:
        response = await self.http.post(self._url(method), json=payload)
        if response.status_code >= 400:
            raise TelegramError(
                f"{method} falhou com HTTP {response.status_code}: {response.text[:300]}"
            )
        return response.json()

    async def send_message(
        self,
        text: str,
        buttons: list[Button] | None = None,
        thread_id: int | None = None,
        chat_id: str | int | None = None,
    ) -> dict:
        buttons = buttons or []
        body = truncate(text)
        payload: dict = {
            "chat_id": self.chat_id if chat_id is None else str(chat_id),
            "text": body,
            "parse_mode": "HTML",
            "disable_web_page_preview": True,
        }
        if thread_id is not None:
            payload["message_thread_id"] = thread_id
        if buttons:
            rows = []
            for button in buttons:
                if button.callback_data:
                    rows.append(
                        [{"text": button.text, "callback_data": button.callback_data}]
                    )
                elif button.url:
                    rows.append([{"text": button.text, "url": button.url}])
            if rows:
                payload["reply_markup"] = json.dumps({"inline_keyboard": rows})

        response = await self.http.post(self._url("sendMessage"), json=payload)

        if response.status_code == 429 and MAX_ATTEMPTS > 1:
            retry_after = _retry_after(response)
            await self._sleep(retry_after)
            response = await self.http.post(self._url("sendMessage"), json=payload)

        if response.status_code == 400 and buttons and _button_rejected(response):
            fallback = _with_links(body, buttons)
            payload.pop("reply_markup", None)
            payload["text"] = fallback
            response = await self.http.post(self._url("sendMessage"), json=payload)

        if response.status_code >= 400:
            raise TelegramError(
                f"sendMessage falhou com HTTP {response.status_code}: {response.text[:300]}"
            )
        return response.json()

    async def get_updates(self, offset: int | None = None) -> list[dict]:
        params: dict[str, int] = {}
        if offset is not None:
            params["offset"] = offset
        response = await self.http.get(self._url("getUpdates"), params=params)
        if response.status_code >= 400:
            raise TelegramError(
                f"getUpdates falhou com HTTP {response.status_code}: {response.text[:300]}"
            )
        return response.json().get("result", [])

    async def answer_callback(self, callback_id: str, text: str) -> dict:
        return await self._post(
            "answerCallbackQuery",
            {"callback_query_id": callback_id, "text": text},
        )


def _retry_after(response: httpx.Response) -> float:
    try:
        parameters = response.json().get("parameters") or {}
        return float(parameters.get("retry_after", 1))
    except (ValueError, AttributeError):
        return 1.0


def _button_rejected(response: httpx.Response) -> bool:
    try:
        description = str(response.json().get("description", ""))
    except (ValueError, AttributeError):
        description = response.text
    lowered = description.lower()
    return "button" in lowered or "url" in lowered


def _with_links(text: str, buttons: list[Button]) -> str:
    links = "\n".join(
        f"{button.text}: {button.url}" for button in buttons if button.url
    )
    return truncate(f"{text}\n\n{links}")

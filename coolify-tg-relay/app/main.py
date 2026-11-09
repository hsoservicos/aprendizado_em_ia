from __future__ import annotations

import asyncio
import contextlib
import hmac
import json
import logging
from contextlib import asynccontextmanager
from datetime import UTC, datetime

import httpx
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.bot import Bot
from app.config import Settings, load_settings
from app.coolify import CoolifyClient
from app.store import Store, build_dedupe_key
from app.telegram import TelegramClient
from app.templates import EVENT_ALIASES, EVENT_IDS, load_templates
from app.worker import Dispatcher, run_forever

IGNORED = {"ok": True, "ignored": True}
ACCEPTED = {"ok": True}
REJECTED = {"ok": False}


def create_app(
    settings: Settings | None = None,
    store: Store | None = None,
    dispatcher: Dispatcher | None = None,
    bot: Bot | None = None,
    start_worker: bool = False,
    http: httpx.AsyncClient | None = None,
) -> FastAPI:
    """Cria a aplicação FastAPI. Use ``build_app`` como factory do uvicorn."""
    settings = settings or load_settings()
    store = store or Store(settings.database_path)

    @asynccontextmanager
    async def lifespan(application: FastAPI):
        tasks: list[asyncio.Task] = []
        if start_worker and dispatcher is not None:
            tasks.append(asyncio.create_task(run_forever(dispatcher)))
        if start_worker and bot is not None:
            tasks.append(asyncio.create_task(bot.run()))
        try:
            yield
        finally:
            for task in tasks:
                task.cancel()
                with contextlib.suppress(asyncio.CancelledError):
                    await task
            if http is not None:
                await http.aclose()

    app = FastAPI(title="coolify-tg-relay", lifespan=lifespan)
    app.state.settings = settings
    app.state.store = store

    @app.post("/hook/{secret}")
    async def hook(secret: str, request: Request):
        if not hmac.compare_digest(secret, settings.hook_secret):
            return JSONResponse(status_code=401, content=REJECTED)

        raw = await request.body()
        try:
            payload = json.loads(raw)
        except (json.JSONDecodeError, UnicodeDecodeError):
            return JSONResponse(status_code=200, content=IGNORED)

        if not isinstance(payload, dict):
            return JSONResponse(status_code=200, content=IGNORED)

        event = str(payload.get("event") or "")
        if event not in EVENT_IDS and event not in EVENT_ALIASES:
            return JSONResponse(status_code=200, content=IGNORED)

        store.enqueue(build_dedupe_key(payload, datetime.now(UTC)), payload)
        return JSONResponse(status_code=200, content=ACCEPTED)

    @app.get("/healthz")
    async def healthz() -> dict[str, object]:
        return {
            "ok": True,
            "queue": store.pending_count(),
            "last_event": store.meta_get("last_event"),
        }

    return app


def build_app() -> FastAPI:
    settings = load_settings()
    logging.basicConfig(
        level=settings.log_level,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    # httpx registra a URL completa em INFO, o que expõe o token do bot nos logs.
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    http = httpx.AsyncClient()
    store = Store(settings.database_path)
    telegram = TelegramClient(settings.telegram_bot_token, settings.telegram_chat_id, http)
    coolify = CoolifyClient(settings.coolify_base_url, settings.coolify_api_token, http)
    dispatcher = Dispatcher(
        store,
        telegram,
        load_templates(),
        coolify=coolify,
        threads=settings.telegram_threads,
    )
    bot = Bot(telegram, coolify, store, settings)
    return create_app(
        settings,
        store=store,
        dispatcher=dispatcher,
        bot=bot,
        start_worker=True,
        http=http,
    )

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

import httpx

DEFAULT_TIMEOUT = 20.0


class CoolifyError(RuntimeError):
    """Falha ao conversar com a API do Coolify."""


class CoolifyClient:
    def __init__(
        self,
        base_url: str,
        token: str,
        http: httpx.AsyncClient,
        timeout: float = DEFAULT_TIMEOUT,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.token = token
        self.http = http
        self.timeout = timeout

    @property
    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/json",
        }

    async def _request(self, method: str, path: str, payload: dict | None = None) -> Any:
        response = await self.http.request(
            method,
            f"{self.base_url}/api/v1{path}",
            headers=self._headers,
            json=payload,
            timeout=self.timeout,
        )
        if response.status_code >= 400:
            raise CoolifyError(
                f"Coolify respondeu HTTP {response.status_code} em {method} {path}: "
                f"{response.text[:300]}"
            )
        if not response.content:
            return {}
        return response.json()

    async def list_applications(self) -> list[dict]:
        return await self._request("GET", "/applications")

    async def get_application(self, uuid: str) -> dict:
        return await self._request("GET", f"/applications/{uuid}")

    async def list_servers(self) -> list[dict]:
        return await self._request("GET", "/servers")

    async def list_deployments(self) -> list[dict]:
        return await self._request("GET", "/deployments")

    async def get_deployment(self, uuid: str) -> dict:
        deployment = await self._request("GET", f"/deployments/{uuid}")
        return _with_duration(deployment)

    async def deploy(self, uuid: str) -> dict:
        return await self._request("POST", "/deploy", {"uuid": uuid})

    async def start(self, uuid: str) -> dict:
        return await self._request("POST", f"/applications/{uuid}/start")

    async def restart(self, uuid: str) -> dict:
        return await self._request("POST", f"/applications/{uuid}/restart")

    async def stop(self, uuid: str) -> dict:
        return await self._request("POST", f"/applications/{uuid}/stop")


def _parse(value: object) -> datetime | None:
    if not value:
        return None
    text = str(value).strip().replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        return None
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=UTC)


def _with_duration(deployment: dict) -> dict:
    result = dict(deployment)
    started = _parse(result.get("created_at"))
    finished = _parse(result.get("finished_at"))
    if started and finished:
        result["duration_seconds"] = max(0, int((finished - started).total_seconds()))
    else:
        result["duration_seconds"] = None
    return result

import json

import httpx
import pytest

from app.coolify import CoolifyClient, CoolifyError

BASE_URL = "http://coolify:8080"
TOKEN = "api-token"
APP_UUID = "app-1"
DEPLOY_UUID = "dep-1"


def _client(responses, expected: list[tuple[str, str]]):
    requests: list[httpx.Request] = []

    async def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        method, path = expected.pop(0)
        assert request.method == method
        assert request.url.path == path
        assert request.headers["authorization"] == f"Bearer {TOKEN}"
        return responses.pop(0)

    http = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    return CoolifyClient(BASE_URL, TOKEN, http), requests, http


async def test_get_deployment_maps_commit_and_duration():
    body = {
        "deployment_uuid": DEPLOY_UUID,
        "application_name": "sound-music-app",
        "commit": "bb24bb9185a7470f18900e9a0835fc9b14966db1",
        "commit_message": "fix: corrige reprodução de faixas",
        "status": "finished",
        "created_at": "2026-11-08T03:22:09.000000Z",
        "finished_at": "2026-11-08T03:24:53.000000Z",
    }
    client, _requests, http = _client(
        [httpx.Response(200, json=body)],
        [("GET", f"/api/v1/deployments/{DEPLOY_UUID}")],
    )

    async with http:
        deployment = await client.get_deployment(DEPLOY_UUID)

    assert deployment["commit"] == body["commit"]
    assert deployment["commit_message"] == body["commit_message"]
    assert deployment["duration_seconds"] == 164
    assert deployment["status"] == "finished"


async def test_deploy_posts_uuid():
    response_body = {
        "deployments": [{"message": "Deploy iniciado", "deployment_uuid": DEPLOY_UUID}]
    }
    client, requests, http = _client(
        [httpx.Response(200, json=response_body)],
        [("POST", "/api/v1/deploy")],
    )

    async with http:
        result = await client.deploy(APP_UUID)

    assert json.loads(requests[0].content) == {"uuid": APP_UUID}
    assert result == response_body


async def test_api_error_raises():
    client, _requests, http = _client(
        [httpx.Response(404, json={"message": "Application not found."})],
        [("GET", f"/api/v1/applications/{APP_UUID}")],
    )

    async with http:
        with pytest.raises(CoolifyError):
            await client.get_application(APP_UUID)

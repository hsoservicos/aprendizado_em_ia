from fastapi.testclient import TestClient

from app.config import Settings
from app.main import create_app

SECRET = "s" * 32


def _app(tmp_path, secret: str = SECRET):
    settings = Settings(
        hook_secret=secret,
        database_path=str(tmp_path / "relay.db"),
    )
    return create_app(settings)


def _payload(event: str = "deployment_success") -> dict:
    return {
        "event": event,
        "deployment_uuid": "dep-1",
        "application_name": "sound-music-app",
        "commit": "bb24bb9185a7470f18900e9a0835fc9b14966db1",
        "created_at": "2026-11-08T03:22:09Z",
        "finished_at": "2026-11-08T03:24:53Z",
    }


def test_valid_secret_enqueues_and_returns_200(tmp_path):
    app = _app(tmp_path)

    with TestClient(app) as client:
        response = client.post(f"/hook/{SECRET}", json=_payload())

    assert response.status_code == 200
    assert response.json() == {"ok": True}
    assert app.state.store.pending_count() == 1


def test_invalid_secret_returns_401(tmp_path):
    app = _app(tmp_path)

    with TestClient(app) as client:
        response = client.post(f"/hook/{'x' * 32}", json=_payload())

    assert response.status_code == 401
    assert response.json() == {"ok": False}
    assert app.state.store.pending_count() == 0


def test_unknown_event_returns_200(tmp_path):
    app = _app(tmp_path)

    with TestClient(app) as client:
        response = client.post(f"/hook/{SECRET}", json=_payload("evento_novo"))

    assert response.status_code == 200
    assert response.json() == {"ok": True, "ignored": True}
    assert app.state.store.pending_count() == 0


def test_malformed_json_returns_200(tmp_path):
    app = _app(tmp_path)

    with TestClient(app) as client:
        response = client.post(
            f"/hook/{SECRET}",
            content=b"{isto nao e json",
            headers={"content-type": "application/json"},
        )

    assert response.status_code == 200
    assert response.json() == {"ok": True, "ignored": True}
    assert app.state.store.pending_count() == 0

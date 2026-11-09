from fastapi.testclient import TestClient

from app.config import Settings
from app.main import create_app


def test_healthz_returns_ok(tmp_path):
    settings = Settings(database_path=str(tmp_path / "relay.db"))
    client = TestClient(create_app(settings))

    response = client.get("/healthz")

    assert response.status_code == 200
    assert response.json() == {"ok": True, "queue": 0, "last_event": None}

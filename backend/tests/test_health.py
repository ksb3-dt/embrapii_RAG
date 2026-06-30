from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

VALID_DEPENDENCY_STATUSES = {"ok", "unavailable", "not_configured"}


def test_health_returns_200() -> None:
    response = client.get("/health")
    assert response.status_code == 200


def test_health_response_shape() -> None:
    response = client.get("/health")
    data = response.json()

    assert data["status"] == "ok"
    assert data["service"] == "backend"
    assert isinstance(data["version"], str)
    assert data["version"]

    dependencies = data["dependencies"]
    assert dependencies["redis"] in VALID_DEPENDENCY_STATUSES
    assert dependencies["qdrant"] in VALID_DEPENDENCY_STATUSES

"""Tests for API route placeholders and schema imports."""

import importlib

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

_LLM_SESSION = {"provider": "claude", "model": "claude-3", "api_key": "key"}

SCHEMA_MODULES = [
    "app.api.schemas.common",
    "app.api.schemas.comparisons",
    "app.api.schemas.documents",
    "app.api.schemas.errors",
    "app.api.schemas.evaluation",
    "app.api.schemas.evidence",
    "app.api.schemas.jobs",
    "app.api.schemas.qa",
    "app.api.schemas.summaries",
]

ROUTE_MODULES = [
    "app.api.routes.comparisons",
    "app.api.routes.documents",
    "app.api.routes.evaluation",
    "app.api.routes.evidence",
    "app.api.routes.health",
    "app.api.routes.jobs",
    "app.api.routes.qa",
    "app.api.routes.summaries",
]

PLACEHOLDER_CASES = [
    ("GET", "/documents"),
    ("POST", "/qa", {"question": "test", **_LLM_SESSION}),
    ("POST", "/summaries", {"document_id": "doc-1", **_LLM_SESSION}),
    (
        "POST",
        "/comparisons",
        {"document_ids": ["doc-1", "doc-2"], **_LLM_SESSION},
    ),
    ("GET", "/jobs/job-1"),
    ("GET", "/evidence/answer-1"),
    ("GET", "/evaluation/questions"),
    ("POST", "/evaluation/runs", _LLM_SESSION),
]


def test_health_still_returns_200() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_schema_modules_import() -> None:
    for module_name in SCHEMA_MODULES:
        importlib.import_module(module_name)


def test_route_modules_import() -> None:
    for module_name in ROUTE_MODULES:
        importlib.import_module(module_name)


def test_placeholder_routes_return_501_with_error_shape() -> None:
    for case in PLACEHOLDER_CASES:
        method, path, *payload = case
        if method == "GET":
            response = client.get(path)
        else:
            response = client.post(path, json=payload[0])

        assert response.status_code == 501, f"{method} {path} expected 501"
        data = response.json()
        assert data["code"] == "NOT_IMPLEMENTED"
        assert isinstance(data["message"], str)
        assert data["message"]
        assert data["details"] == {}


def test_document_upload_placeholder_returns_501() -> None:
    response = client.post(
        "/documents",
        files={"file": ("report.pdf", b"%PDF-1.4 placeholder", "application/pdf")},
    )
    assert response.status_code == 501
    data = response.json()
    assert data["code"] == "NOT_IMPLEMENTED"
    assert isinstance(data["message"], str)
    assert data["details"] == {}


def test_delete_document_placeholder_returns_501() -> None:
    response = client.delete("/documents/doc-1")
    assert response.status_code == 501
    data = response.json()
    assert data["code"] == "NOT_IMPLEMENTED"
    assert data["details"] == {}

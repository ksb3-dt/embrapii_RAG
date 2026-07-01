"""Tests for application service dependency wiring."""

import importlib
import inspect

from fastapi.testclient import TestClient

from app.core import dependencies
from app.main import app

client = TestClient(app)

SERVICE_PROVIDER_NAMES = [
    "get_document_ingestion_service",
    "get_question_answering_service",
    "get_report_summary_service",
    "get_report_comparison_service",
    "get_evidence_audit_service",
    "get_job_service",
    "get_evaluation_service",
]

ROUTE_MODULES = [
    "app.api.routes.comparisons",
    "app.api.routes.documents",
    "app.api.routes.evaluation",
    "app.api.routes.evidence",
    "app.api.routes.jobs",
    "app.api.routes.qa",
    "app.api.routes.summaries",
]

FORBIDDEN_ROUTE_IMPORT_PREFIXES = (
    "app.infrastructure",
    "qdrant",
    "redis",
    "rq",
    "langchain",
    "pymupdf",
    "fitz",
)


def test_dependency_providers_return_service_instances() -> None:
    for provider_name in SERVICE_PROVIDER_NAMES:
        provider = getattr(dependencies, provider_name)
        instance = provider()
        assert instance is not None
        second_instance = provider()
        assert isinstance(second_instance, type(instance))


def test_dependency_aliases_are_defined() -> None:
    alias_names = [
        "DocumentIngestionServiceDep",
        "QuestionAnsweringServiceDep",
        "ReportSummaryServiceDep",
        "ReportComparisonServiceDep",
        "EvidenceAuditServiceDep",
        "JobServiceDep",
        "EvaluationServiceDep",
    ]
    for alias_name in alias_names:
        assert hasattr(dependencies, alias_name)


def test_routes_use_dependency_providers_not_infrastructure() -> None:
    for module_name in ROUTE_MODULES:
        module = importlib.import_module(module_name)
        source = inspect.getsource(module)
        assert "app.core.dependencies" in source
        for prefix in FORBIDDEN_ROUTE_IMPORT_PREFIXES:
            assert prefix not in source, (
                f"{module_name} imports infrastructure: {prefix}"
            )


def test_wired_qa_route_still_returns_501() -> None:
    response = client.post(
        "/qa",
        json={
            "question": "test",
            "provider": "claude",
            "model": "claude-3",
            "api_key": "key",
        },
    )
    assert response.status_code == 501
    data = response.json()
    assert data["code"] == "NOT_IMPLEMENTED"
    assert data["details"] == {}


def test_wired_evaluation_questions_route_still_returns_501() -> None:
    response = client.get("/evaluation/questions")
    assert response.status_code == 501
    data = response.json()
    assert data["code"] == "NOT_IMPLEMENTED"

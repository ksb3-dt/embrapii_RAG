"""Tests for application service placeholder modules."""

import importlib
import inspect

import pytest

from app.application.exceptions import NotImplementedApplicationError
from app.application.services.document_ingestion_service import DocumentIngestionService
from app.application.services.evaluation_service import EvaluationService
from app.application.services.evidence_audit_service import EvidenceAuditService
from app.application.services.job_service import JobService
from app.application.services.question_answering_service import QuestionAnsweringService
from app.application.services.report_comparison_service import ReportComparisonService
from app.application.services.report_summary_service import ReportSummaryService
from app.domain.models.job import JobType

SERVICE_MODULES = [
    "app.application.services.document_ingestion_service",
    "app.application.services.question_answering_service",
    "app.application.services.report_summary_service",
    "app.application.services.report_comparison_service",
    "app.application.services.evidence_audit_service",
    "app.application.services.evaluation_service",
    "app.application.services.job_service",
]

USE_CASE_MODULES = [
    "app.application.use_cases.ingest_document",
    "app.application.use_cases.ask_question",
    "app.application.use_cases.summarize_report",
    "app.application.use_cases.compare_reports",
]

_LLM_KWARGS = {"provider": "claude", "model": "claude-3", "api_key": "session-key"}


def test_service_modules_import() -> None:
    for module_name in SERVICE_MODULES:
        importlib.import_module(module_name)


def test_use_case_modules_import() -> None:
    for module_name in USE_CASE_MODULES:
        importlib.import_module(module_name)


def test_services_do_not_import_fastapi_or_api_schemas() -> None:
    forbidden_prefixes = ("fastapi", "app.api")
    for module_name in SERVICE_MODULES:
        module = importlib.import_module(module_name)
        source_path = inspect.getsourcefile(module)
        assert source_path is not None
        source = inspect.getsource(module)
        for line in source.splitlines():
            stripped = line.strip()
            if stripped.startswith("from ") or stripped.startswith("import "):
                for prefix in forbidden_prefixes:
                    assert prefix not in stripped, (
                        f"{module_name} imports forbidden module: {stripped}"
                    )


@pytest.mark.parametrize(
    ("service_factory", "call"),
    [
        (
            DocumentIngestionService,
            lambda service: service.ingest_document("report.pdf", b"%PDF"),
        ),
        (
            QuestionAnsweringService,
            lambda service: service.answer_question(
                "Pergunta?",
                provider="claude",
                model="m",
                api_key="k",
            ),
        ),
        (
            ReportSummaryService,
            lambda service: service.summarize_report("doc-1", **_LLM_KWARGS),
        ),
        (
            ReportComparisonService,
            lambda service: service.compare_reports(("doc-1", "doc-2"), **_LLM_KWARGS),
        ),
        (
            EvidenceAuditService,
            lambda service: service.get_answer_evidence("answer-1"),
        ),
        (
            EvaluationService,
            lambda service: service.list_questions(),
        ),
        (
            EvaluationService,
            lambda service: service.run_evaluation((), **_LLM_KWARGS),
        ),
        (
            JobService,
            lambda service: service.get_job_status("job-1"),
        ),
        (
            JobService,
            lambda service: service.create_job(
                JobType.INGEST_DOCUMENT,
                document_id="doc-1",
            ),
        ),
    ],
)
def test_placeholder_service_methods_raise_not_implemented(
    service_factory,
    call,
) -> None:
    service = service_factory()
    with pytest.raises(NotImplementedApplicationError) as exc_info:
        call(service)
    assert exc_info.value.message

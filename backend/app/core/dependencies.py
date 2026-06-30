from typing import Annotated

from fastapi import Depends

from app.application.services.document_ingestion_service import DocumentIngestionService
from app.application.services.evaluation_service import EvaluationService
from app.application.services.evidence_audit_service import EvidenceAuditService
from app.application.services.job_service import JobService
from app.application.services.question_answering_service import QuestionAnsweringService
from app.application.services.report_comparison_service import ReportComparisonService
from app.application.services.report_summary_service import ReportSummaryService
from app.core.config import Settings, get_settings


def get_settings_dependency() -> Settings:
    """Placeholder para injeção de dependências estáticas em rotas."""
    return get_settings()


def get_document_ingestion_service() -> DocumentIngestionService:
    """Provide the document ingestion application service."""
    return DocumentIngestionService()


def get_question_answering_service() -> QuestionAnsweringService:
    """Provide the question answering application service."""
    return QuestionAnsweringService()


def get_report_summary_service() -> ReportSummaryService:
    """Provide the report summary application service."""
    return ReportSummaryService()


def get_report_comparison_service() -> ReportComparisonService:
    """Provide the report comparison application service."""
    return ReportComparisonService()


def get_evidence_audit_service() -> EvidenceAuditService:
    """Provide the evidence audit application service."""
    return EvidenceAuditService()


def get_job_service() -> JobService:
    """Provide the background job application service."""
    return JobService()


def get_evaluation_service() -> EvaluationService:
    """Provide the golden-set evaluation application service."""
    return EvaluationService()


SettingsDep = Annotated[Settings, Depends(get_settings_dependency)]
DocumentIngestionServiceDep = Annotated[
    DocumentIngestionService, Depends(get_document_ingestion_service)
]
QuestionAnsweringServiceDep = Annotated[
    QuestionAnsweringService, Depends(get_question_answering_service)
]
ReportSummaryServiceDep = Annotated[
    ReportSummaryService, Depends(get_report_summary_service)
]
ReportComparisonServiceDep = Annotated[
    ReportComparisonService, Depends(get_report_comparison_service)
]
EvidenceAuditServiceDep = Annotated[
    EvidenceAuditService, Depends(get_evidence_audit_service)
]
JobServiceDep = Annotated[JobService, Depends(get_job_service)]
EvaluationServiceDep = Annotated[EvaluationService, Depends(get_evaluation_service)]

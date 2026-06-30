"""Domain model for background work tracked by the application."""

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum


class JobStatus(StrEnum):
    """Lifecycle status of a background job."""

    PENDING = "pending"
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class JobType(StrEnum):
    """Kind of asynchronous work represented by a job."""

    INGEST_DOCUMENT = "ingest_document"
    SUMMARIZE_REPORT = "summarize_report"
    COMPARE_REPORTS = "compare_reports"
    RUN_EVALUATION = "run_evaluation"


@dataclass(frozen=True)
class Job:
    """Background work item independent of queue infrastructure."""

    id: str
    job_type: JobType
    status: JobStatus
    created_at: datetime | None = None
    updated_at: datetime | None = None
    error_message: str | None = None
    document_id: str | None = None

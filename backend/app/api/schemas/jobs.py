"""Request and response schemas for background job APIs."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel

JobStatusValue = Literal["pending", "queued", "running", "completed", "failed"]
JobTypeValue = Literal[
    "ingest_document",
    "summarize_report",
    "compare_reports",
    "run_evaluation",
]


class JobResponse(BaseModel):
    """Background work item status returned by job endpoints."""

    id: str
    job_type: JobTypeValue
    status: JobStatusValue
    created_at: datetime | None = None
    updated_at: datetime | None = None
    error_message: str | None = None
    document_id: str | None = None

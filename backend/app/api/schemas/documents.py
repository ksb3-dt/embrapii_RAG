"""Request and response schemas for document APIs."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

DocumentStatusValue = Literal["pending", "processing", "indexed", "failed"]


class DocumentResponse(BaseModel):
    """Uploaded report metadata returned by document endpoints."""

    id: str
    filename: str
    status: DocumentStatusValue
    title: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class DocumentListResponse(BaseModel):
    """Collection of uploaded reports."""

    documents: list[DocumentResponse] = Field(default_factory=list)


class DocumentUploadResponse(BaseModel):
    """Response after accepting a document upload."""

    document: DocumentResponse
    job_id: str | None = None

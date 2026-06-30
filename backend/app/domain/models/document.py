"""Domain models for uploaded reports and extracted pages."""

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum


class DocumentStatus(StrEnum):
    """Lifecycle status of an uploaded report."""

    PENDING = "pending"
    PROCESSING = "processing"
    INDEXED = "indexed"
    FAILED = "failed"


@dataclass(frozen=True)
class Document:
    """Uploaded report with stable identity and ingestion status."""

    id: str
    filename: str
    source_path: str
    status: DocumentStatus
    title: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


@dataclass(frozen=True)
class DocumentPage:
    """Extracted text for a single 1-based PDF page."""

    document_id: str
    page_number: int
    text: str

    def __post_init__(self) -> None:
        if self.page_number < 1:
            msg = "page_number must be 1-based"
            raise ValueError(msg)

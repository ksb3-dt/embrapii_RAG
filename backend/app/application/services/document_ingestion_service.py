"""Coordinates document upload, parsing, chunking, and indexing workflows."""

from app.application.exceptions import raise_not_implemented
from app.domain.models.document import Document


class DocumentIngestionService:
    """Application service for ingesting uploaded PDF reports."""

    def ingest_document(self, filename: str, content: bytes) -> Document:
        """Accept a PDF upload and enqueue or run the ingestion workflow."""
        raise_not_implemented("Document endpoints are not implemented yet.")

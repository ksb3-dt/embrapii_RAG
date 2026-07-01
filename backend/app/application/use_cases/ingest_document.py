"""Use case wrapper for document ingestion."""

from app.application.services.document_ingestion_service import DocumentIngestionService
from app.domain.models.document import Document


class IngestDocumentUseCase:
    """Thin boundary for the document ingestion workflow."""

    def __init__(self, ingestion_service: DocumentIngestionService) -> None:
        self._ingestion_service = ingestion_service

    def execute(self, filename: str, content: bytes) -> Document:
        """Run the ingestion workflow for one uploaded PDF."""
        return self._ingestion_service.ingest_document(filename, content)

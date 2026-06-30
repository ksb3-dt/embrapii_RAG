"""Port for extracting text from uploaded PDF reports."""

from typing import Protocol

from app.domain.models.document import DocumentPage


class DocumentParser(Protocol):
    """Parses a PDF file into page-level text content."""

    def parse(self, file_path: str) -> list[DocumentPage]:
        """Extract 1-based pages from the PDF at ``file_path``."""
        ...

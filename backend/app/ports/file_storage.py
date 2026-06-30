"""Port for storing uploaded report PDFs."""

from typing import Protocol


class FileStorage(Protocol):
    """Persists and resolves document files on local or remote storage."""

    def save_pdf(self, filename: str, content: bytes) -> str:
        """Store PDF bytes and return a storage-relative path."""
        ...

    def delete_document_file(self, relative_path: str) -> None:
        """Remove a stored document file."""
        ...

    def resolve_document_path(self, relative_path: str) -> str:
        """Resolve a storage-relative path to an absolute filesystem path."""
        ...

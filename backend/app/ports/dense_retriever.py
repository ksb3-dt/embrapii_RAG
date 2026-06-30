"""Port for semantic vector retrieval."""

from dataclasses import dataclass
from typing import Protocol

from app.domain.models.chunk import EvidenceChunk


@dataclass(frozen=True)
class RetrievalFilters:
    """Optional constraints applied during retrieval."""

    document_ids: tuple[str, ...] | None = None


class DenseRetriever(Protocol):
    """Retrieves ranked evidence candidates using dense vector search."""

    def retrieve(
        self,
        query: str,
        filters: RetrievalFilters | None,
        limit: int,
    ) -> list[EvidenceChunk]:
        """Return evidence chunks ordered by semantic relevance."""
        ...

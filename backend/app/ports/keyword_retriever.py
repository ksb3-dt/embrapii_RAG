"""Port for exact keyword retrieval."""

from typing import Protocol

from app.domain.models.chunk import EvidenceChunk
from app.ports.dense_retriever import RetrievalFilters


class KeywordRetriever(Protocol):
    """Retrieves ranked evidence candidates using keyword or exact-term search."""

    def retrieve(
        self,
        query: str,
        filters: RetrievalFilters | None,
        limit: int,
    ) -> list[EvidenceChunk]:
        """Return evidence chunks ordered by keyword relevance."""
        ...

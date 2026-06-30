"""Port for combining multiple retrieval channels."""

from typing import Protocol

from app.domain.models.chunk import EvidenceChunk
from app.ports.dense_retriever import RetrievalFilters


class FusionRetriever(Protocol):
    """Retrieves evidence by fusing dense and keyword candidate lists."""

    def retrieve(
        self,
        query: str,
        filters: RetrievalFilters | None,
        limit: int,
    ) -> list[EvidenceChunk]:
        """Return fused evidence chunks ready for grounded generation."""
        ...

"""Request and response schemas for evidence audit APIs."""

from typing import Literal

from pydantic import BaseModel, Field

from app.api.schemas.common import CitationResponse

RetrievalSourceValue = Literal["dense", "keyword", "fusion"]
ChunkTypeValue = Literal["text", "table", "caption", "infographic_text"]


class EvidenceChunkResponse(BaseModel):
    """Retrieved chunk with ranking metadata for audit views."""

    chunk_id: str
    document_id: str
    page_number: int
    text: str
    retrieval_source: RetrievalSourceValue
    citation: CitationResponse
    document_title: str | None = None
    rank: int | None = None
    score: float | None = None
    chunk_type: ChunkTypeValue = "text"


class EvidenceResponse(BaseModel):
    """Evidence chunks supporting a generated answer."""

    answer_id: str
    evidence: list[EvidenceChunkResponse] = Field(default_factory=list)

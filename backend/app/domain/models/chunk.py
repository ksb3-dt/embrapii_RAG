"""Domain models for chunks, citations, and retrieval evidence."""

from dataclasses import dataclass
from enum import StrEnum


class ChunkType(StrEnum):
    """Kind of content represented by a stored chunk."""

    TEXT = "text"
    TABLE = "table"
    CAPTION = "caption"
    INFOGRAPHIC_TEXT = "infographic_text"


class RetrievalSource(StrEnum):
    """Retrieval channel that produced an evidence chunk."""

    DENSE = "dense"
    KEYWORD = "keyword"
    FUSION = "fusion"


@dataclass(frozen=True)
class Citation:
    """Page-level citation pointing back to a report."""

    document_id: str
    page_number: int
    document_title: str | None = None

    def __post_init__(self) -> None:
        if self.page_number < 1:
            msg = "page_number must be 1-based"
            raise ValueError(msg)


@dataclass(frozen=True)
class DocumentChunk:
    """Indexed chunk with citation metadata for later audit views."""

    document_id: str
    chunk_id: str
    page_number: int
    text: str
    chunk_type: ChunkType
    section_title: str | None = None
    source_file_path: str | None = None

    def __post_init__(self) -> None:
        if self.page_number < 1:
            msg = "page_number must be 1-based"
            raise ValueError(msg)


@dataclass(frozen=True)
class EvidenceChunk:
    """Retrieved chunk with ranking metadata for grounded answers."""

    chunk_id: str
    document_id: str
    page_number: int
    text: str
    retrieval_source: RetrievalSource
    citation: Citation
    document_title: str | None = None
    rank: int | None = None
    score: float | None = None
    chunk_type: ChunkType = ChunkType.TEXT

    def __post_init__(self) -> None:
        if self.page_number < 1:
            msg = "page_number must be 1-based"
            raise ValueError(msg)

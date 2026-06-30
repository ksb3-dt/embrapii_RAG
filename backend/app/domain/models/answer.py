"""Domain models for grounded answers and confidence indicators."""

from dataclasses import dataclass, field
from enum import StrEnum

from app.domain.models.chunk import Citation, EvidenceChunk


class ConfidenceLevel(StrEnum):
    """Discrete confidence band for a generated answer."""

    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    NOT_FOUND = "not_found"


@dataclass(frozen=True)
class Answer:
    """Grounded answer with citations, evidence, and confidence metadata."""

    text: str
    confidence_level: ConfidenceLevel
    citations: tuple[Citation, ...] = field(default_factory=tuple)
    evidence: tuple[EvidenceChunk, ...] = field(default_factory=tuple)
    is_not_found: bool = False
    is_low_confidence: bool = False

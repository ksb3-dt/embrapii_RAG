"""Request and response schemas for question-answering APIs."""

from typing import Literal

from pydantic import BaseModel, Field

from app.api.schemas.common import CitationResponse, LlmSessionFields

ConfidenceLevelValue = Literal["high", "medium", "low", "not_found"]


class QaRequest(LlmSessionFields):
    """Grounded question against the indexed report corpus."""

    question: str
    document_ids: list[str] = Field(default_factory=list)


class QaResponse(BaseModel):
    """Grounded answer with confidence and page-level citations."""

    answer_id: str
    text: str
    confidence_level: ConfidenceLevelValue
    citations: list[CitationResponse] = Field(default_factory=list)
    is_not_found: bool = False
    is_low_confidence: bool = False

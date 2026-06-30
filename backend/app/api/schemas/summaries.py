"""Request and response schemas for report summary APIs."""

from pydantic import BaseModel, Field

from app.api.schemas.common import CitationResponse, LlmSessionFields


class SummaryRequest(LlmSessionFields):
    """Request to summarize one indexed report."""

    document_id: str


class SummaryResponse(BaseModel):
    """Structured summary aligned with the MVP output sections."""

    document_id: str
    executive_summary: str
    main_findings: list[str] = Field(default_factory=list)
    relevant_numbers_kpis: list[str] = Field(default_factory=list)
    risks_gaps_or_limitations: list[str] = Field(default_factory=list)
    notable_evidence: list[CitationResponse] = Field(default_factory=list)
    what_was_not_clear: list[str] = Field(default_factory=list)

"""Request and response schemas for multi-report comparison APIs."""

from pydantic import BaseModel, Field

from app.api.schemas.common import CitationResponse, LlmSessionFields


class ComparisonRequest(LlmSessionFields):
    """Request to compare multiple indexed reports."""

    document_ids: list[str] = Field(min_length=2)


class ComparisonEvidenceByReport(BaseModel):
    """Evidence grouped by report for comparison output."""

    document_id: str
    citations: list[CitationResponse] = Field(default_factory=list)


class ComparisonResponse(BaseModel):
    """Structured comparison aligned with the MVP output sections."""

    document_ids: list[str]
    high_level_conclusion: str
    similarities: list[str] = Field(default_factory=list)
    differences: list[str] = Field(default_factory=list)
    trends_over_time: list[str] = Field(default_factory=list)
    evidence_by_report: list[ComparisonEvidenceByReport] = Field(default_factory=list)
    uncertainties_or_missing_data: list[str] = Field(default_factory=list)

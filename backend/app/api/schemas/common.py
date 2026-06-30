"""Shared API schema building blocks."""

from typing import Literal

from pydantic import BaseModel

LlmProviderValue = Literal["claude", "gemini", "openai", "deepseek"]


class LlmSessionFields(BaseModel):
    """Per-request LLM provider, model, and API key fields."""

    provider: LlmProviderValue
    model: str
    api_key: str


class CitationResponse(BaseModel):
    """Page-level citation pointing back to a report."""

    document_id: str
    page_number: int
    document_title: str | None = None

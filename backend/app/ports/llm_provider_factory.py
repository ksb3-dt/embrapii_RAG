"""Port for creating request-scoped LLM provider adapters."""

from enum import StrEnum
from typing import Protocol

from app.ports.llm_provider import LLMProvider


class LLMProviderName(StrEnum):
    """Supported final-answer providers exposed in the MVP UI."""

    CLAUDE = "claude"
    GEMINI = "gemini"
    OPENAI = "openai"
    DEEPSEEK = "deepseek"


class LLMProviderFactory(Protocol):
    """Builds LLM adapters from per-request provider, model, and API key."""

    def create(
        self,
        provider: LLMProviderName | str,
        model: str,
        api_key: str,
    ) -> LLMProvider:
        """Return a provider adapter without persisting the API key."""
        ...

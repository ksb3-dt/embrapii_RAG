"""Port for final-answer language model providers."""

from typing import Protocol


class LLMProvider(Protocol):
    """Generates grounded answers from prompts and optional retrieved context."""

    def generate(self, prompt: str, context: str | None = None) -> str:
        """Return model-generated text for the given prompt and context."""
        ...

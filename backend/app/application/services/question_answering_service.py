"""Coordinates grounded question answering across indexed reports."""

from app.application.exceptions import raise_not_implemented
from app.domain.models.answer import Answer


class QuestionAnsweringService:
    """Application service for retrieval-augmented question answering."""

    def answer_question(
        self,
        question: str,
        document_ids: tuple[str, ...] = (),
        *,
        provider: str,
        model: str,
        api_key: str,
    ) -> Answer:
        """Answer a user question using retrieved report evidence."""
        raise_not_implemented("Question answering is not implemented yet.")

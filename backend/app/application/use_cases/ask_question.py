"""Use case wrapper for question answering."""

from app.application.services.question_answering_service import QuestionAnsweringService
from app.domain.models.answer import Answer


class AskQuestionUseCase:
    """Thin boundary for grounded question answering."""

    def __init__(self, question_answering_service: QuestionAnsweringService) -> None:
        self._question_answering_service = question_answering_service

    def execute(
        self,
        question: str,
        document_ids: tuple[str, ...] = (),
        *,
        provider: str,
        model: str,
        api_key: str,
    ) -> Answer:
        """Answer a user question against indexed reports."""
        return self._question_answering_service.answer_question(
            question,
            document_ids,
            provider=provider,
            model=model,
            api_key=api_key,
        )

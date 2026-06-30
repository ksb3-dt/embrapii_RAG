"""Coordinates golden-set evaluation workflows."""

from app.application.exceptions import raise_not_implemented
from app.domain.models.evaluation import EvaluationQuestion


class EvaluationService:
    """Application service for evaluation question listing and runs."""

    def list_questions(self) -> list[EvaluationQuestion]:
        """Return configured golden-set evaluation questions."""
        raise_not_implemented("Evaluation endpoints are not implemented yet.")

    def run_evaluation(
        self,
        question_ids: tuple[str, ...] = (),
        *,
        provider: str,
        model: str,
        api_key: str,
    ) -> None:
        """Execute the golden-set evaluation workflow."""
        raise_not_implemented("Evaluation endpoints are not implemented yet.")

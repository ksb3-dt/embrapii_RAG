"""Domain models for golden-set evaluation records."""

from dataclasses import dataclass
from enum import StrEnum


class EvaluationStatus(StrEnum):
    """Lifecycle status of an evaluation run."""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass(frozen=True)
class EvaluationQuestion:
    """Golden-set question used to validate retrieval and answering."""

    id: str
    question_text: str
    expected_document_ids: tuple[str, ...] = ()
    tags: tuple[str, ...] = ()


@dataclass(frozen=True)
class EvaluationResult:
    """Recorded outcome for one golden-set question without scoring logic."""

    question_id: str
    answer_text: str
    status: EvaluationStatus
    passed: bool | None = None
    notes: str | None = None

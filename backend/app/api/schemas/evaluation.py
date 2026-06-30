"""Request and response schemas for golden-set evaluation APIs."""

from typing import Literal

from pydantic import BaseModel, Field

from app.api.schemas.common import LlmSessionFields

EvaluationStatusValue = Literal["pending", "running", "completed", "failed"]


class EvaluationQuestionResponse(BaseModel):
    """Golden-set question exposed by evaluation endpoints."""

    id: str
    question_text: str
    expected_document_ids: list[str] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)


class EvaluationQuestionListResponse(BaseModel):
    """Collection of golden-set questions."""

    questions: list[EvaluationQuestionResponse] = Field(default_factory=list)


class EvaluationRunRequest(LlmSessionFields):
    """Request to execute the golden-set evaluation workflow."""

    question_ids: list[str] = Field(default_factory=list)


class EvaluationResultResponse(BaseModel):
    """Outcome for one golden-set question."""

    question_id: str
    answer_text: str
    status: EvaluationStatusValue
    passed: bool | None = None
    notes: str | None = None


class EvaluationRunResponse(BaseModel):
    """Summary of an evaluation run."""

    run_id: str
    status: EvaluationStatusValue
    results: list[EvaluationResultResponse] = Field(default_factory=list)

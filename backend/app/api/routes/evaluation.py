"""Golden-set evaluation route placeholders."""

from fastapi import APIRouter

from app.api.schemas.errors import ApplicationErrorResponse, not_implemented_response
from app.api.schemas.evaluation import EvaluationRunRequest

router = APIRouter(tags=["evaluation"])

_NOT_IMPLEMENTED_MESSAGE = "Evaluation endpoints are not implemented yet."
_PLACEHOLDER_RESPONSES = {501: {"model": ApplicationErrorResponse}}


@router.get("/evaluation/questions", responses=_PLACEHOLDER_RESPONSES)
def list_evaluation_questions():
    return not_implemented_response(_NOT_IMPLEMENTED_MESSAGE)


@router.post("/evaluation/runs", responses=_PLACEHOLDER_RESPONSES)
def run_evaluation(request: EvaluationRunRequest):
    return not_implemented_response(_NOT_IMPLEMENTED_MESSAGE)

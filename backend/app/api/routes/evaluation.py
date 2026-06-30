"""Golden-set evaluation route placeholders."""

from fastapi import APIRouter

from app.api.route_helpers import call_placeholder_service
from app.api.schemas.errors import ApplicationErrorResponse
from app.api.schemas.evaluation import EvaluationRunRequest
from app.core.dependencies import EvaluationServiceDep

router = APIRouter(tags=["evaluation"])

_PLACEHOLDER_RESPONSES = {501: {"model": ApplicationErrorResponse}}


@router.get("/evaluation/questions", responses=_PLACEHOLDER_RESPONSES)
def list_evaluation_questions(evaluation_service: EvaluationServiceDep):
    return call_placeholder_service(evaluation_service.list_questions)


@router.post("/evaluation/runs", responses=_PLACEHOLDER_RESPONSES)
def run_evaluation(
    request: EvaluationRunRequest,
    evaluation_service: EvaluationServiceDep,
):
    return call_placeholder_service(
        evaluation_service.run_evaluation,
        tuple(request.question_ids),
        provider=request.provider,
        model=request.model,
        api_key=request.api_key,
    )

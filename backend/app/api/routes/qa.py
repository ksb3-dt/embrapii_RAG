"""Question-answering route placeholder."""

from fastapi import APIRouter

from app.api.route_helpers import call_placeholder_service
from app.api.schemas.errors import ApplicationErrorResponse
from app.api.schemas.qa import QaRequest
from app.core.dependencies import QuestionAnsweringServiceDep

router = APIRouter(tags=["qa"])


@router.post("/qa", responses={501: {"model": ApplicationErrorResponse}})
def ask_question(
    request: QaRequest,
    qa_service: QuestionAnsweringServiceDep,
):
    return call_placeholder_service(
        qa_service.answer_question,
        request.question,
        tuple(request.document_ids),
        provider=request.provider,
        model=request.model,
        api_key=request.api_key,
    )

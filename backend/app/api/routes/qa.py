"""Question-answering route placeholder."""

from fastapi import APIRouter

from app.api.schemas.errors import ApplicationErrorResponse, not_implemented_response
from app.api.schemas.qa import QaRequest

router = APIRouter(tags=["qa"])

_NOT_IMPLEMENTED_MESSAGE = "Question answering is not implemented yet."


@router.post("/qa", responses={501: {"model": ApplicationErrorResponse}})
def ask_question(request: QaRequest):
    return not_implemented_response(_NOT_IMPLEMENTED_MESSAGE)

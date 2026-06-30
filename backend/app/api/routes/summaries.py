"""Report summary route placeholder."""

from fastapi import APIRouter

from app.api.schemas.errors import ApplicationErrorResponse, not_implemented_response
from app.api.schemas.summaries import SummaryRequest

router = APIRouter(tags=["summaries"])

_NOT_IMPLEMENTED_MESSAGE = "Report summaries are not implemented yet."


@router.post("/summaries", responses={501: {"model": ApplicationErrorResponse}})
def summarize_report(request: SummaryRequest):
    return not_implemented_response(_NOT_IMPLEMENTED_MESSAGE)

"""Multi-report comparison route placeholder."""

from fastapi import APIRouter

from app.api.schemas.comparisons import ComparisonRequest
from app.api.schemas.errors import ApplicationErrorResponse, not_implemented_response

router = APIRouter(tags=["comparisons"])

_NOT_IMPLEMENTED_MESSAGE = "Report comparisons are not implemented yet."


@router.post("/comparisons", responses={501: {"model": ApplicationErrorResponse}})
def compare_reports(request: ComparisonRequest):
    return not_implemented_response(_NOT_IMPLEMENTED_MESSAGE)

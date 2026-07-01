"""Report summary route placeholder."""

from fastapi import APIRouter

from app.api.route_helpers import call_placeholder_service
from app.api.schemas.errors import ApplicationErrorResponse
from app.api.schemas.summaries import SummaryRequest
from app.core.dependencies import ReportSummaryServiceDep

router = APIRouter(tags=["summaries"])


@router.post("/summaries", responses={501: {"model": ApplicationErrorResponse}})
def summarize_report(
    request: SummaryRequest,
    summary_service: ReportSummaryServiceDep,
):
    return call_placeholder_service(
        summary_service.summarize_report,
        request.document_id,
        provider=request.provider,
        model=request.model,
        api_key=request.api_key,
    )

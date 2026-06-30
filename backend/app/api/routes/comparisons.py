"""Multi-report comparison route placeholder."""

from fastapi import APIRouter

from app.api.route_helpers import call_placeholder_service
from app.api.schemas.comparisons import ComparisonRequest
from app.api.schemas.errors import ApplicationErrorResponse
from app.core.dependencies import ReportComparisonServiceDep

router = APIRouter(tags=["comparisons"])


@router.post("/comparisons", responses={501: {"model": ApplicationErrorResponse}})
def compare_reports(
    request: ComparisonRequest,
    comparison_service: ReportComparisonServiceDep,
):
    return call_placeholder_service(
        comparison_service.compare_reports,
        tuple(request.document_ids),
        provider=request.provider,
        model=request.model,
        api_key=request.api_key,
    )

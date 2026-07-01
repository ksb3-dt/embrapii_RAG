"""Background job status route placeholder."""

from fastapi import APIRouter

from app.api.route_helpers import call_placeholder_service
from app.api.schemas.errors import ApplicationErrorResponse
from app.core.dependencies import JobServiceDep

router = APIRouter(tags=["jobs"])


@router.get("/jobs/{job_id}", responses={501: {"model": ApplicationErrorResponse}})
def get_job(job_id: str, job_service: JobServiceDep):
    return call_placeholder_service(job_service.get_job_status, job_id)

"""Background job status route placeholder."""

from fastapi import APIRouter

from app.api.schemas.errors import ApplicationErrorResponse, not_implemented_response

router = APIRouter(tags=["jobs"])

_NOT_IMPLEMENTED_MESSAGE = "Job status endpoints are not implemented yet."


@router.get("/jobs/{job_id}", responses={501: {"model": ApplicationErrorResponse}})
def get_job(job_id: str):
    return not_implemented_response(_NOT_IMPLEMENTED_MESSAGE)

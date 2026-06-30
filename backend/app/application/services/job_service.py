"""Coordinates background job creation and status lookup."""

from app.application.exceptions import raise_not_implemented
from app.domain.models.job import Job, JobType


class JobService:
    """Application service for queue-backed background work."""

    def get_job_status(self, job_id: str) -> Job:
        """Return the current status of a background job."""
        raise_not_implemented("Job status endpoints are not implemented yet.")

    def create_job(
        self,
        job_type: JobType,
        document_id: str | None = None,
    ) -> Job:
        """Create and enqueue a new background job."""
        raise_not_implemented("Job status endpoints are not implemented yet.")

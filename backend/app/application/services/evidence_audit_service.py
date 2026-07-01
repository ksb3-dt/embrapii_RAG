"""Coordinates evidence lookup for answer audit views."""

from app.application.exceptions import raise_not_implemented
from app.domain.models.answer import Answer


class EvidenceAuditService:
    """Application service for retrieving stored answer evidence."""

    def get_answer_evidence(self, answer_id: str) -> Answer:
        """Load evidence chunks and citations supporting an answer."""
        raise_not_implemented("Evidence audit endpoints are not implemented yet.")

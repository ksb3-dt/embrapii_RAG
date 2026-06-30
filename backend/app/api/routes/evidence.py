"""Evidence audit route placeholder."""

from fastapi import APIRouter

from app.api.route_helpers import call_placeholder_service
from app.api.schemas.errors import ApplicationErrorResponse
from app.core.dependencies import EvidenceAuditServiceDep

router = APIRouter(tags=["evidence"])

_PLACEHOLDER_RESPONSES = {501: {"model": ApplicationErrorResponse}}


@router.get("/evidence/{answer_id}", responses=_PLACEHOLDER_RESPONSES)
def get_evidence(answer_id: str, evidence_service: EvidenceAuditServiceDep):
    return call_placeholder_service(evidence_service.get_answer_evidence, answer_id)

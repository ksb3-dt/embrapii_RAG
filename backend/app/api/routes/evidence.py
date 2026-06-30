"""Evidence audit route placeholder."""

from fastapi import APIRouter

from app.api.schemas.errors import ApplicationErrorResponse, not_implemented_response

router = APIRouter(tags=["evidence"])

_NOT_IMPLEMENTED_MESSAGE = "Evidence audit endpoints are not implemented yet."
_PLACEHOLDER_RESPONSES = {501: {"model": ApplicationErrorResponse}}


@router.get("/evidence/{answer_id}", responses=_PLACEHOLDER_RESPONSES)
def get_evidence(answer_id: str):
    return not_implemented_response(_NOT_IMPLEMENTED_MESSAGE)

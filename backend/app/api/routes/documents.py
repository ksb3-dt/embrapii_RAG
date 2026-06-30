"""Document upload, list, and delete route placeholders."""

from fastapi import APIRouter, UploadFile

from app.api.schemas.errors import ApplicationErrorResponse, not_implemented_response

router = APIRouter(tags=["documents"])

_NOT_IMPLEMENTED_MESSAGE = "Document endpoints are not implemented yet."
_PLACEHOLDER_RESPONSES = {501: {"model": ApplicationErrorResponse}}


@router.post("/documents", responses=_PLACEHOLDER_RESPONSES)
async def upload_document(file: UploadFile):
    return not_implemented_response(_NOT_IMPLEMENTED_MESSAGE)


@router.get("/documents", responses=_PLACEHOLDER_RESPONSES)
def list_documents():
    return not_implemented_response(_NOT_IMPLEMENTED_MESSAGE)


@router.delete("/documents/{document_id}", responses=_PLACEHOLDER_RESPONSES)
def delete_document(document_id: str):
    return not_implemented_response(_NOT_IMPLEMENTED_MESSAGE)

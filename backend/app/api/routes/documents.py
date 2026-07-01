"""Document upload, list, and delete route placeholders."""

from fastapi import APIRouter, UploadFile

from app.api.route_helpers import call_placeholder_service
from app.api.schemas.errors import ApplicationErrorResponse, not_implemented_response
from app.core.dependencies import DocumentIngestionServiceDep

router = APIRouter(tags=["documents"])

_NOT_IMPLEMENTED_MESSAGE = "Document endpoints are not implemented yet."
_PLACEHOLDER_RESPONSES = {501: {"model": ApplicationErrorResponse}}


@router.post("/documents", responses=_PLACEHOLDER_RESPONSES)
async def upload_document(
    file: UploadFile,
    ingestion_service: DocumentIngestionServiceDep,
):
    content = await file.read()
    return call_placeholder_service(
        ingestion_service.ingest_document,
        file.filename or "upload.pdf",
        content,
    )


@router.get("/documents", responses=_PLACEHOLDER_RESPONSES)
def list_documents(_ingestion_service: DocumentIngestionServiceDep):
    return not_implemented_response(_NOT_IMPLEMENTED_MESSAGE)


@router.delete("/documents/{document_id}", responses=_PLACEHOLDER_RESPONSES)
def delete_document(document_id: str, _ingestion_service: DocumentIngestionServiceDep):
    return not_implemented_response(_NOT_IMPLEMENTED_MESSAGE)

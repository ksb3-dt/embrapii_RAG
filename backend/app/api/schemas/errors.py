"""Shared application error response schema and helpers."""

from typing import Any

from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field


class ApplicationErrorResponse(BaseModel):
    """Consistent JSON shape for application-level errors."""

    code: str
    message: str
    details: dict[str, Any] = Field(default_factory=dict)


def not_implemented_response(message: str) -> JSONResponse:
    """Return HTTP 501 with the standard application error shape."""
    body = ApplicationErrorResponse(
        code="NOT_IMPLEMENTED",
        message=message,
        details={},
    )
    return JSONResponse(status_code=501, content=body.model_dump())

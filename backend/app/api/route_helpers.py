"""Helpers for thin placeholder route handlers."""

from collections.abc import Callable
from typing import Any

from fastapi.responses import JSONResponse

from app.api.schemas.errors import not_implemented_response
from app.application.exceptions import NotImplementedApplicationError


def call_placeholder_service(
    service_call: Callable[..., Any],
    /,
    *args: Any,
    **kwargs: Any,
) -> JSONResponse:
    """Map placeholder service failures to the standard HTTP 501 response."""
    try:
        service_call(*args, **kwargs)
    except NotImplementedApplicationError as exc:
        return not_implemented_response(exc.message)
    msg = "Placeholder service did not raise a not-implemented error."
    raise RuntimeError(msg)

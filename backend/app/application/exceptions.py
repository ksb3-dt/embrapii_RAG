"""Application-level exceptions for workflow coordination."""

from typing import Never


class NotImplementedApplicationError(Exception):
    """Raised when an application workflow is not implemented yet."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


def raise_not_implemented(message: str) -> Never:
    """Raise a consistent not-implemented application error."""
    raise NotImplementedApplicationError(message)

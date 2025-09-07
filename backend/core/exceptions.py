"""
Custom exceptions for backend error handling.
"""


class BackendError(Exception):
    """Base exception for backend errors."""

    pass


class NotFoundError(BackendError):
    """Raised when a resource is not found."""

    pass


class ValidationError(BackendError):
    """Raised when input validation fails."""

    pass


class UpstreamServiceError(BackendError):
    """Raised when an upstream service fails."""

    pass


class AuthorizationError(BackendError):
    """Raised when authorization fails."""

    pass

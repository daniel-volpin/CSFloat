"""
Custom exceptions for backend error handling.
"""


class BackendError(Exception):
    """Base exception for backend errors."""


class NotFoundError(BackendError):
    """Raised when a resource is not found."""


class ValidationError(BackendError):
    """Raised when input validation fails."""


class UpstreamServiceError(BackendError):
    """Raised when an upstream service fails."""


class AuthorizationError(BackendError):
    """Raised when authorization fails."""

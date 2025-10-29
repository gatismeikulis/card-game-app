from .app_exception import AppException


class DomainException(AppException):
    """Base class for all domain-level exceptions."""

    code: str = "domain_error"
    detail: str = "A domain error occurred."

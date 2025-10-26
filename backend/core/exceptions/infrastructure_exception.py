from .app_exception import AppException


class InfrastructureException(AppException):
    """Base class for all infrastructure-level errors (e.g. DB, cache, network)."""

    code: str = "infrastructure_error"
    message: str = "An infrastructure error occurred."

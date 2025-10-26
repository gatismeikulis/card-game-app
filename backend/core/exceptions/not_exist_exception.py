from .app_exception import AppException


class NotExistException(AppException):
    """Exception raised when a resource does not exist."""

    code: str = "not_exist_error"
    message: str = "A resource does not exist."

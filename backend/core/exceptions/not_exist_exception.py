from typing import Any, override
from .app_exception import AppException


class NotExistException(AppException):
    """Exception raised when a resource does not exist."""

    code: str = "resource_not_exist"
    detail: str = "A resource does not exist."

    @override
    def to_dict_minimal(self) -> dict[str, Any]:
        return {
            "code": self.code,
            "reason": self.reason,
            "context": self.context,
        }

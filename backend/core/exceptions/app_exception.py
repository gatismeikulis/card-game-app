from typing import Any, Self


class AppException(Exception):
    """Base app exception with standard serialization and context."""

    code: str = "error"
    message: str = "An unexpected error occurred."

    def __init__(self, message: str | None = None, reason: str | None = None, *, context: dict[str, Any] | None = None):
        # `reason` is an identifier (like "table_full" or "card_not_allowed_to_play" or "card_parsing_error")
        # `message` is human-readable and optional override
        super().__init__(message or self.message)
        self.reason = reason or self.code
        self.context = context or {}

    def with_context(self, **extra: Any) -> Self:
        self.context.update(extra)
        return self

    def to_dict(self) -> dict[str, Any]:
        return {
            "error": self.code,
            "reason": self.reason,
            "message": str(self),
            "context": self.context,
        }

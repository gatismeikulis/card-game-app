from typing import Any, Self


class AppException(Exception):
    """Base app exception with standard serialization and context."""

    code: str = "error"
    detail: str = "An unexpected error occurred."

    def __init__(self, detail: str | None = None, reason: str | None = None, *, context: dict[str, Any] | None = None):
        # `reason` is an identifier (like "table_full" or "card_not_allowed_to_play" or "card_parsing_error")
        # `detail` is human-readable and optional override
        super().__init__(detail or self.detail)
        self.reason = reason or self.code
        self.context = context or {}

    def with_context(self, **extra: Any) -> Self:
        self.context.update(extra)
        return self

    def to_dict(self) -> dict[str, Any]:
        return {
            "code": self.code,
            "reason": self.reason,
            "detail": str(self),
            "context": self.context,
        }

    # minimal dictionary to send to the client, without exposing potentially sensitive information
    def to_dict_minimal(self) -> dict[str, Any]:
        return {}

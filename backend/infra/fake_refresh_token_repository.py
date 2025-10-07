from datetime import datetime

from backend.domain.core.user_id import UserId


class FakeRefreshTokenRepository:
    def __init__(self):
        self._tokens: dict[str, tuple[UserId, datetime]] = {}

    def save_refresh_token(self, user_id: UserId, token: str, expires_at: datetime) -> bool:
        self._tokens[token] = (user_id, expires_at)
        return True

    def find_user_id_by_token(self, token: str) -> UserId | None:
        print("find_user_id_by_token", token)
        print("self._tokens", self._tokens)
        return self._tokens[token][0] if token in self._tokens else None

    def delete_token(self, token: str) -> bool: ...

    def delete_tokens_by_user_id(self, user_id: UserId) -> int: ...

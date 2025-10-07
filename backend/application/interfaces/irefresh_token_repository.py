from datetime import datetime
from typing import Protocol

from backend.domain.core.user_id import UserId


class IRefreshTokenRepository(Protocol):

    # in concrete implementation, include methods like _to_entity, _to_model

    def delete_token(self, token: str) -> bool: ...

    def delete_tokens_by_user_id(self, user_id: UserId) -> int: ...

    def save_refresh_token(self, user_id: UserId, token: str, expires_at: datetime) -> bool: ...

    def find_user_id_by_token(self, token: str) -> UserId | None: ...

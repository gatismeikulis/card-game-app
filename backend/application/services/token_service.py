import secrets
from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
from backend.application.interfaces.irefresh_token_repository import IRefreshTokenRepository
from backend.domain.core.user import Role, UserIdentity
from backend.domain.core.user_id import UserId


class TokenService:
    def __init__(self, refresh_token_repository: IRefreshTokenRepository, jwt_secret: str, jwt_algorithm: str):
        self._refresh_token_repository: IRefreshTokenRepository = refresh_token_repository
        self._jwt_secret: str = jwt_secret
        self._jwt_algorithm: str = jwt_algorithm

    def _generate_random_token(self) -> str:
        return secrets.token_hex(32)

    def _encode_jwt(self, payload: dict[str, Any], secret: str, algorithm: str) -> str:
        return jwt.encode(payload, secret, algorithm=algorithm)

    def _decode_jwt(self, token: str, secret: str, algorithm: str) -> dict[str, Any]:
        return jwt.decode(token, secret, algorithms=[algorithm])

    def create_access_token(self, user_identity: UserIdentity) -> str:
        token_payload: dict[str, Any] = {
            "sub": user_identity.id.value.hex,
            "name": user_identity.username,
            "role": user_identity.role.value,
            "exp": int(datetime.now(timezone.utc).timestamp() + 900),  # 15 minutes
            "iat": int(datetime.now(timezone.utc).timestamp()),
        }
        token = self._encode_jwt(token_payload, self._jwt_secret, self._jwt_algorithm)
        return token

    def create_refresh_token(self, user_id: UserId) -> str:
        token = self._generate_random_token()
        expires_at = datetime.now(timezone.utc) + timedelta(days=30)
        _ = self._refresh_token_repository.save_refresh_token(user_id, token, expires_at)  # ignore return value for now
        return token

    def extract_user_identity(self, token: str) -> UserIdentity:
        payload = self._decode_jwt(token, self._jwt_secret, self._jwt_algorithm)
        user_id = UserId.from_str(payload["sub"])
        username = payload["name"]
        role = Role(payload["role"])
        user_identity = UserIdentity(id=user_id, username=username, role=role)
        return user_identity

    def verify_refresh_token(self, token: str) -> UserId | None:
        user_id = self._refresh_token_repository.find_user_id_by_token(token)
        return user_id

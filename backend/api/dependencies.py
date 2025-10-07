from typing import Annotated

from backend.application.services.token_service import TokenService
from backend.application.services.user_service import UserService
from backend.domain.core.user import UserIdentity
from backend.infra.fake_refresh_token_repository import FakeRefreshTokenRepository
from backend.infra.fake_user_repository import FakeUserRepository
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# TODO: use secrets fron config, use pydantic_settings maybe...
_fake_jwt_secret = "secret"
_fake_jwt_algorithm = "HS256"


_user_repository = FakeUserRepository()
_refresh_token_repository = FakeRefreshTokenRepository()

_user_service: UserService = UserService(user_repository=_user_repository)

_token_service: TokenService = TokenService(
    refresh_token_repository=_refresh_token_repository,
    jwt_secret=_fake_jwt_secret,
    jwt_algorithm=_fake_jwt_algorithm,
)


def get_user_service() -> UserService:
    return _user_service


def get_token_service() -> TokenService:
    return _token_service


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], token_service: Annotated[TokenService, Depends(get_token_service)]
) -> UserIdentity:
    try:
        return token_service.extract_user_identity(token)
    except Exception as e:  # TODO: should not use generic exception handling
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials: " + str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )

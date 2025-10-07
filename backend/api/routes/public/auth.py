from typing import Annotated

from backend.api.dependencies import get_token_service, get_user_service
from backend.api.schemas.user import AccessTokenResponse, CreateUserRequest, CreateUserResponse
from backend.application.dtos.user import CreateUserData
from backend.application.services.token_service import TokenService
from backend.application.services.user_service import UserService
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/login")
async def login(
    response: Response,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    user_service: Annotated[UserService, Depends(get_user_service)],
    token_service: Annotated[TokenService, Depends(get_token_service)],
) -> AccessTokenResponse:
    user = user_service.authenticate(form_data.username, form_data.password)

    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    access_token = token_service.create_access_token(user.identity)
    refresh_token = token_service.create_refresh_token(user.identity.id)

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,  # Cannot be accessed by JavaScript
        secure=False,  # Only sent over HTTPS TODO: change to True in production
        samesite="none",  # Disabled CSRF protection for development TODO: use "lax" or "strict" in production
        max_age=2592000,  # 30 days in seconds
        path="/auth/refresh",  # Only sent to auth endpoints
    )

    return AccessTokenResponse(access_token=access_token, token_type="bearer")


@router.post("/register")
async def register_new_user(
    user_data: CreateUserRequest,
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> CreateUserResponse:
    create_user_data = CreateUserData(
        name=user_data.name,
        username=user_data.username,
        email=user_data.email,
        password=user_data.password,
    )
    user = user_service.create_user(create_user_data)

    if not user:
        raise HTTPException(status_code=400, detail="Failed to create user")  # TODO: better error message

    return CreateUserResponse(username=user.identity.username)


@router.post("/refresh")
async def refresh(
    request: Request,
    token_service: Annotated[TokenService, Depends(get_token_service)],
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> AccessTokenResponse:
    refresh_token = request.cookies.get("refresh_token")

    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token missing.")

    user_id = token_service.verify_refresh_token(refresh_token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid refresh token.")

    user = user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid refresh token.")

    new_access_token = token_service.create_access_token(user.identity)

    return AccessTokenResponse(access_token=new_access_token, token_type="bearer")


# TODO: add logout endpoint

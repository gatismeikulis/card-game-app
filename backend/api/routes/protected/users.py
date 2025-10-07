from typing import Annotated

from backend.api.dependencies import get_current_user, get_user_service
from backend.api.schemas.user import GetUsersResponse, UserProfileResponse
from backend.application.services.user_service import UserService
from backend.domain.core.user import Role, UserIdentity
from fastapi import APIRouter, Depends, HTTPException

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get("/")
async def get_users(
    user_identity: Annotated[UserIdentity, Depends(get_current_user)],
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> GetUsersResponse:
    if user_identity.role != Role.ADMIN:
        raise HTTPException(status_code=403, detail="You are not authorized to access this resource")
    users = user_service.get_users()

    return GetUsersResponse(usernames=[user.identity.username for user in users])


@router.get("/me")
async def get_user_profile(
    user_identity: Annotated[UserIdentity, Depends(get_current_user)],
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> UserProfileResponse:
    user = user_service.get_user_by_id(user_identity.id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user_profile = UserProfileResponse(
        id=user.identity.id.value.hex,
        username=user.identity.username,
        email=user.email,
        role=user.identity.role.value,
    )

    return user_profile

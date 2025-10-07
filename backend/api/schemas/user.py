from collections.abc import Sequence

from pydantic import BaseModel, EmailStr


class CreateUserRequest(BaseModel):
    name: str
    username: str
    email: EmailStr
    password: str


class CreateUserResponse(BaseModel):
    username: str


class UserProfileResponse(BaseModel):
    id: str  # UserId
    username: str
    email: EmailStr
    role: str  # Role


class AccessTokenResponse(BaseModel):
    access_token: str
    token_type: str


class GetUsersResponse(BaseModel):
    usernames: Sequence[str]

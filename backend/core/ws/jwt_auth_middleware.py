from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async

User = get_user_model()


@database_sync_to_async
def get_user_from_token(token_string: str):
    """Get user from JWT token. Raises TokenError if token is invalid, expired, or unsafe."""
    try:
        access_token = AccessToken(token_string)
        user_id = access_token.get("user_id")

        return User.objects.get(pk=user_id)
    except (TokenError, InvalidToken, User.DoesNotExist) as e:
        raise TokenError("Invalid or expired authentication token.") from e


class JWTAuthMiddleware(BaseMiddleware):
    """
    Custom middleware to authenticate WebSocket connections using JWT tokens.
    Token can be provided as auth header:
    Authorization: Bearer <token>
    """

    async def __call__(self, scope, receive, send):
        # Extract token from authorization header
        headers = dict(scope.get("headers", []))

        token_string = None

        auth_header = headers.get(b"authorization", b"").decode()
        if auth_header.startswith("Bearer "):
            token_string = auth_header.split("Bearer ")[1]

        # Authenticate user
        if token_string:
            try:
                scope["user"] = await get_user_from_token(token_string)
            except TokenError as e:
                scope["auth_error"] = str(e)
        else:
            scope["user"] = AnonymousUser()

        return await super().__call__(scope, receive, send)

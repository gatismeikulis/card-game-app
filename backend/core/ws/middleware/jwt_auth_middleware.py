from typing import override
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from urllib.parse import parse_qs

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
    Token must be provided as query parameter: ?token=<token>
    """

    @override
    async def __call__(self, scope, receive, send):
        token_string = None

        query_string = scope.get("query_string", b"").decode()
        if query_string:
            query_params = parse_qs(query_string)
            token_list = query_params.get("token", [])
            if token_list:
                token_string = token_list[0]

        if token_string:
            try:
                user = await get_user_from_token(token_string)
                scope["user"] = user
            except TokenError as e:
                scope["auth_error"] = str(e)
        else:
            scope["user"] = AnonymousUser()

        return await super().__call__(scope, receive, send)

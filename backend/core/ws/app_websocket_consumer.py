import json
from typing import Any, override

from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.contrib.auth import get_user_model
from core.exceptions.app_exception import AppException

User = get_user_model()


class AppWebSocketConsumer(AsyncJsonWebsocketConsumer):
    @override
    async def connect(self):
        # close connection if auth error raised
        auth_error = self.scope.get("auth_error")
        user = self.scope.get("user")
        if auth_error or not user:
            await self.close(code=4003, reason=auth_error)
            return

        # user still can be AnonymousUser
        self.user: User = user
        await self.accept()

    @override
    async def receive(self, text_data: str | None = None, bytes_data: bytes | None = None, **kwargs):
        """Handle raw text_data and parse JSON manually with error handling"""
        if text_data is None:
            return

        try:
            content: dict[str, Any] = json.loads(text_data)
        except json.JSONDecodeError:
            # Send error back to client but keep connection alive
            error = AppException(reason="invalid_json", detail="WS message must be valid JSON").with_context(
                text_data=text_data
            )
            await self.send_json(error.to_dict())
            return

        await self.receive_json(content, **kwargs)

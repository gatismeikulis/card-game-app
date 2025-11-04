import json
from typing import Any, override

from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.contrib.auth import get_user_model
from ..exceptions.infrastructure_exception import InfrastructureException
from ..exceptions.app_exception import AppException

User = get_user_model()


class AppWebSocketConsumer(AsyncJsonWebsocketConsumer):
    @override
    async def connect(self):
        await self._safe_execute(self._on_connect)

    @override
    async def receive(self, text_data: str | None = None, bytes_data: bytes | None = None, **kwargs):
        await self._safe_execute(self.on_receive, text_data, bytes_data, **kwargs)

    async def _safe_execute(self, func, *args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            if not isinstance(e, AppException):
                e = InfrastructureException(detail=str(e)).with_context(error=e)
            print(f"Error in consumer: {e.to_dict()}")
            await self.send_json({"type": "error", "data": e.to_dict_minimal()})

    async def _on_connect(self):
        auth_error = self.scope.get("auth_error")
        user = self.scope.get("user")
        if auth_error or not user:
            await self.close(code=4003, reason=auth_error)
            return

        # user still can be AnonymousUser
        self.user: User = user
        await self.accept()

    async def on_receive(self, text_data: str | None = None, bytes_data: bytes | None = None, **kwargs):
        if text_data is None:
            return
        try:
            content: dict[str, Any] = json.loads(text_data)
            await self.receive_json(content, **kwargs)
        except json.JSONDecodeError:
            raise AppException(reason="invalid_json", detail="WS message must be valid JSON").with_context(
                text_data=text_data
            )

from typing import Any, override

from core.ws.app_websocket_consumer import AppWebSocketConsumer


class GameTableWebSocketConsumer(AppWebSocketConsumer):
    @override
    async def connect(self):
        await super().connect()

        self.table_id: str = self.scope["url_route"]["kwargs"]["table_id"]
        self.table_group_name: str = f"table_{self.table_id}"
        await self.channel_layer.group_add(self.table_group_name, self.channel_name)

    @override
    async def disconnect(self, code: int):
        await self.channel_layer.group_discard(self.table_group_name, self.channel_name)

    @override
    async def receive_json(self, content: dict[str, Any], **kwargs):
        """Handle parsed JSON messages"""

        await self.channel_layer.group_send(
            self.table_group_name, {"type": "table.action", "message": f"test-{content}"}
        )

    async def table_action(self, event: dict[str, Any]):
        """Handle group messages"""
        message = event["message"]
        # Use send_json instead of manual json.dumps
        await self.send_json({"message": f"From ${self.user.username}: {message}"})

from typing import Any, override

from core.exceptions.app_exception import AppException
from core.ws.app_websocket_consumer import AppWebSocketConsumer
from channels.db import database_sync_to_async
from .dependencies import table_manager


class GameTableWebSocketConsumer(AppWebSocketConsumer):
    @override
    async def connect(self):
        self.table_id: str = self.scope["url_route"]["kwargs"]["table_id"]

        # Validate table exists BEFORE accepting the connection
        try:
            table = await database_sync_to_async(table_manager.get_table)(self.table_id)
            self.game_name = table.config.game_name
            self.group_name = f"table_{self.game_name.value}_{self.table_id}"
        except AppException as e:
            await self.close(code=4004, reason=str(e))
            return

        await super().connect()

        await self.send_json(
            {"type": "info", "data": f"WS connection to '{self.game_name.value}' table {self.table_id} established"}
        )
        await self.channel_layer.group_add(self.group_name, self.channel_name)

    @override
    async def disconnect(self, code: int):
        # Only discard if we successfully joined (group_name exists)
        if hasattr(self, "group_name"):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    @override
    async def receive_json(self, content: dict[str, Any], **kwargs):
        """Handle parsed JSON messages"""

        # check if content contains "type" key
        # type key can be take_turn, take_regular_turn, chat_message, join_table, leave_table, add_bot, remove_bot

        table = await database_sync_to_async(table_manager.get_table)(self.table_id)

        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "table.action",
                "message": f"from {self.user.username or 'anonymous'}: {content}",
                "table": table.to_dict(),
            },
        )

    async def table_action(self, event: dict[str, Any]):
        """Handle group messages"""
        message = event["message"]
        table = event["table"]
        await self.send_json({"message": message, "table": table})

from collections.abc import Sequence
from typing import Any, override

from .domain.game_table_action import GameTableAction
from .serializers import (
    AddBotRequestSerializer,
    JoinGameTableRequestSerializer,
    RemoveBotRequestSerializer,
    TakeRegularTurnRequestSerializer,
)
from game.common.game_event import GameEvent
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

        action = GameTableAction.from_str(content.get("action", "none"))
        data = content.get("data", {})

        events: Sequence[GameEvent] = []

        match action:
            case GameTableAction.TAKE_REGULAR_TURN:
                serializer = TakeRegularTurnRequestSerializer(data=data)
                _ = serializer.is_valid(raise_exception=True)

                events, table = await database_sync_to_async(table_manager.take_regular_turn)(
                    table_id=self.table_id, user_id=self.user.pk, raw_command=serializer.validated_data
                )
            case GameTableAction.TAKE_AUTOMATIC_TURN:
                events, table = await database_sync_to_async(table_manager.take_automatic_turn)(
                    table_id=self.table_id, initiated_by=self.user.pk
                )

            case GameTableAction.JOIN_TABLE:
                serializer = JoinGameTableRequestSerializer(data=data)
                _ = serializer.is_valid(raise_exception=True)

                table = await database_sync_to_async(table_manager.join_table)(
                    table_id=self.table_id,
                    user=self.user,
                    preferred_seat_number=serializer.validated_data["preferred_seat"],
                )
            case GameTableAction.LEAVE_TABLE:
                table = await database_sync_to_async(table_manager.leave_table)(
                    table_id=self.table_id, user_id=self.user.pk
                )
            case GameTableAction.ADD_BOT:
                serializer = AddBotRequestSerializer(data=data)
                _ = serializer.is_valid(raise_exception=True)
                table = await database_sync_to_async(table_manager.add_bot_player)(
                    table_id=self.table_id, iniated_by=self.user.pk, options=serializer.validated_data
                )
            case GameTableAction.REMOVE_BOT:
                serializer = RemoveBotRequestSerializer(data=data)
                _ = serializer.is_valid(raise_exception=True)
                table = await database_sync_to_async(table_manager.remove_bot_player)(
                    table_id=self.table_id,
                    iniated_by=self.user.pk,
                    seat_number_to_remove=serializer.validated_data["seat_number"],
                )
            case GameTableAction.START_GAME:
                events, table = await database_sync_to_async(table_manager.start_game)(
                    table_id=self.table_id, iniated_by=self.user.pk
                )

        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "table.action",
                "game_events": [event.to_dict() for event in events],
                "public_table_data": table.to_public_dict(),
                "private_table_data": {p.user_id: table.to_public_dict(p.seat_number) for p in table.players},
            },
        )

    async def table_action(self, event: dict[str, Any]):
        """Handle group messages"""
        game_events = event["game_events"]
        table_data = event["private_table_data"].get(self.user.pk, event["public_table_data"])
        await self.send_json({"type": "table_action", "data": {"game_events": game_events, "table_data": table_data}})

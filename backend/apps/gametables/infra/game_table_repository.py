from typing import override
from django.db import transaction
from django.utils import timezone

from ..models import (
    GameTableSnapshot,
    GameTablePlayer,
    TableConfig as TableConfigModel,
    GameConfig as GameConfigModel,
)
from ..application.igame_table_repository import IGameTableRepository
from ..domain.game_table import GameTable
from .game_table_deserializer import GameTableDeserializer


class GameTableRepository(IGameTableRepository):
    @transaction.atomic
    @override
    def create(self, game_table: GameTable) -> str:
        # Create game table snapshot
        game_table_snapshot = GameTableSnapshot.objects.create(
            id=game_table.id,
            game_name=game_table.config.game_name.value,
            status=game_table.status.value,
            owner_id=game_table.owner_id,
            data=game_table.to_dict(),
        )

        # Create game configs
        for config_key, config_value in game_table.config.table_config.to_dict().items():
            _ = TableConfigModel.objects.create(
                game_table=game_table_snapshot,
                config_key=config_key,
                data=config_value,
            )

        # Create game configs
        for config_key, config_value in game_table.config.game_config.to_dict().items():
            _ = GameConfigModel.objects.create(
                game_table=game_table_snapshot,
                config_key=config_key,
                data=config_value,
            )

        # No GameTablePlayers creation, because there is no players at the moment when table is created

        return game_table.id

    @transaction.atomic
    @override
    def update(self, game_table: GameTable) -> None:
        updated_rows = GameTableSnapshot.objects.filter(id=game_table.id).update(
            game_name=game_table.config.game_name.value,
            status=game_table.status.value,
            owner_id=game_table.owner_id,
            data=game_table.to_dict(),
            updated_at=timezone.now(),
        )
        # deletes all players from the table and reinserts new ones
        _ = GameTablePlayer.objects.filter(game_table_id=game_table.id).delete()
        for player in game_table.players:
            _ = GameTablePlayer.objects.create(
                game_table_id=game_table.id,
                user_id=player.user_id,
                screen_name=player.screen_name,
                bot_strategy_kind=player.bot_strategy.kind.value if player.bot_strategy else None,
            )

        # configs do not change during the game_table's life cycle, so we do not need to update them

        if updated_rows < 1:
            raise ValueError(f"Game table with id {game_table.id} not found")

    @override
    def update_after_turn(self, game_table: GameTable, last_event_sequence_number: int) -> None:
        updated_rows = GameTableSnapshot.objects.filter(id=game_table.id).update(
            data=game_table.to_dict(),
            status=game_table.status.value,
            last_event_sequence_number=last_event_sequence_number,
            updated_at=timezone.now(),
        )
        if updated_rows < 1:
            raise ValueError(f"Game table with id {game_table.id} not found")

    @override
    def delete(self, id: str) -> None:
        _ = GameTableSnapshot.objects.filter(id=id).delete()

    @override
    def find_by_id(self, id: str) -> GameTable:
        try:
            game_table_snapshot = GameTableSnapshot.objects.get(id=id)
            game_table = GameTableDeserializer.deserialize_table(game_table_snapshot.data)
            return game_table
        except GameTableSnapshot.DoesNotExist:
            raise ValueError(f"Game table with id {id} not found")
        except Exception as e:
            raise ValueError(f"Error deserializing game table: {e}")

    @override
    def find_many(self) -> list[GameTableSnapshot]:
        query_set = (
            GameTableSnapshot.objects.select_related("owner")
            .prefetch_related("game_table_players", "game_configs", "table_configs")
            .order_by("-created_at")
        )

        return list(query_set.all())

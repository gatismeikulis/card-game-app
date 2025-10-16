import json
from typing import Any, override
from django.db import transaction

from ..domain.table_status import TableStatus
from ..models import (
    GameTableSnapshot,
    GameTablePlayer,
    TableConfig as TableConfigModel,
    GameConfig as GameConfigModel,
)
from ..application.igame_table_repository import FindByIdResult, IGameTableRepository
from ..domain.game_table import GameTable
from .game_table_deserializer import GameTableDeserializer


class GameTableRepository(IGameTableRepository):
    """
    Hybrid repository:
    - SQL: authoritative metadata store (browse/filter, history).
    - In-memory dict: acts as Redis-like cache for the full domain object JSON.
    """

    def __init__(self):
        self._cache: dict[str, str] = {}

    def _deserialize_table(self, json_str: str) -> GameTable:
        data: dict[str, Any] = json.loads(json_str)
        return GameTableDeserializer.deserialize_table(data)

    @transaction.atomic
    @override
    def create(self, game_table: GameTable) -> str:
        game_table_data = game_table.to_dict()
        game_table_json_str = json.dumps(game_table_data)

        # Cache
        self._cache[game_table.id] = game_table_json_str

        # Create game table snapshot
        game_table_snapshot = GameTableSnapshot.objects.create(
            id=game_table.id,
            game_name=game_table.config.game_name.value,
            status=game_table.status.value,
            owner_id=game_table.owner_id,
            data=game_table_data,
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
    def update(self, game_table: GameTable) -> str:
        status = game_table.status

        game_table_data = game_table.to_dict()

        game_table_json_str = json.dumps(game_table_data)

        # Update Cache
        self._cache[game_table.id] = game_table_json_str

        # update game table snapshot only if game status is NOT IN_PROGRESS
        if status != TableStatus.IN_PROGRESS:
            game_table_snapshot, _ = GameTableSnapshot.objects.update_or_create(
                id=game_table.id,
                defaults={
                    "game_name": game_table.config.game_name.value,
                    "status": game_table.status.value,
                    "owner_id": game_table.owner_id,
                    "data": game_table_data,
                },
            )
            # deletes all players from the table and reinserts new ones
            _ = GameTablePlayer.objects.filter(game_table=game_table_snapshot).delete()
            for player in game_table.players:
                _ = GameTablePlayer.objects.create(
                    game_table=game_table_snapshot,
                    user_id=player.user_id,
                    screen_name=player.screen_name,
                    bot_strategy_kind=player.bot_strategy.kind.value if player.bot_strategy else None,
                )

        # Configs do not change during the game life cycle, so we do not need to update them

        return game_table.id

    @transaction.atomic
    @override
    def delete(self, id: str) -> str:
        # TODO: think if we need to delete the table from the database...
        # maybe just mark it as finished/cancelled/deleted/aborted and keep it for history...
        _ = GameTableSnapshot.objects.filter(id=id).delete()
        _ = self._cache.pop(id, None)
        return id

    @override
    def find_by_id(self, id: str) -> FindByIdResult:
        # Try cache
        cached = self._cache.get(id)
        if cached is not None:
            return FindByIdResult(game_table=self._deserialize_table(cached), from_cache=True)

        # Fallback to SQL snapshot
        try:
            snapshot = GameTableSnapshot.objects.get(id=id)
        except GameTableSnapshot.DoesNotExist:
            raise ValueError(f"Game table with id {id} not found")

        return FindByIdResult(game_table=self._deserialize_table(json.dumps(snapshot.data)), from_cache=False)

    @override
    def find_many(self) -> list[GameTableSnapshot]:
        """
        Browse via SQL only.
        """
        query_set = (
            GameTableSnapshot.objects.select_related("owner")
            .prefetch_related("game_table_players", "game_configs", "table_configs")
            .order_by("-created_at")
        )

        return list(query_set.all())

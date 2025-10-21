import json
from typing import Any, override
from django.db import transaction
from django.core.cache import cache

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
        self._cache_timeout: int = 3600  # 1 hour TODO: make this configurable

    def _key(self, table_id: str) -> str:
        return f"game_table_{table_id}"

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

    @override
    def update_in_cache(self, game_table: GameTable) -> bool:
        try:
            data = game_table.to_dict()
            json_data = json.dumps(data)
            cache.set(self._key(game_table.id), json_data, timeout=self._cache_timeout)
            return True
        except Exception as e:
            print(f"Cache save failed: {e}")
            _ = cache.delete(self._key(game_table.id))
            return False

    @transaction.atomic
    @override
    def update_in_db(self, game_table: GameTable) -> None:
        game_table_snapshot, _ = GameTableSnapshot.objects.update_or_create(
            id=game_table.id,
            defaults={
                "game_name": game_table.config.game_name.value,
                "status": game_table.status.value,
                "owner_id": game_table.owner_id,
                "data": game_table.to_dict(),
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

        # configs do not change during the game_table's life cycle, so we do not need to update them

        return None

    @override
    def delete(self, id: str) -> str:
        # Only delete not-started tables from db...
        # Other tables should be marked as finished/cancelled/deleted/aborted and kept for history...
        # Delete from cache always
        return id

    @override
    def find_by_id(self, id: str) -> FindByIdResult:
        # Try cache
        try:
            cached = cache.get(self._key(id))
            if cached is not None:
                data: dict[str, Any] = json.loads(cached)
                game_table = GameTableDeserializer.deserialize_table(data)
                return FindByIdResult(game_table=game_table, from_cache=True)
        except Exception as e:
            print(f"Cache get failed: {e}")

        # Fallback to SQL snapshot
        try:
            snapshot = GameTableSnapshot.objects.get(id=id)
        except GameTableSnapshot.DoesNotExist:
            raise ValueError(f"Game table with id {id} not found")

        return FindByIdResult(game_table=GameTableDeserializer.deserialize_table(snapshot.data), from_cache=False)

    @override
    def find_many(self) -> list[GameTableSnapshot]:
        query_set = (
            GameTableSnapshot.objects.select_related("owner")
            .prefetch_related("game_table_players", "game_configs", "table_configs")
            .order_by("-created_at")
        )

        return list(query_set.all())

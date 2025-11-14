from typing import Callable, override
from collections.abc import Sequence
from django.db import transaction
from django.db.models import QuerySet
from django.utils import timezone
from core.exceptions.not_exist_exception import NotExistException
from core.exceptions.infrastructure_exception import InfrastructureException
from game.common.game_event import GameEvent
from ..models import (
    GameEventModel,
    GameTableModel,
    PlayerModel,
    TableConfigModel,
    GameConfigModel,
)
from ..application.igame_table_repository import IGameTableRepository
from ..domain.game_table import GameTable
from .game_table_deserializer import GameTableDeserializer


class GameTableRepository(IGameTableRepository):
    @transaction.atomic
    @override
    def create(self, game_table: GameTable) -> str:
        try:
            # Create game table
            db_game_table = GameTableModel.objects.create(
                id=game_table.id,
                game_name=game_table.config.game_name.value,
                status=game_table.status.value,
                owner_id=game_table.owner_id,
                snapshot=game_table.to_dict(),
            )

            # Create game configs
            for config_key, value in game_table.config.table_config.to_dict().items():
                _ = TableConfigModel.objects.create(
                    game_table=db_game_table,
                    config_key=config_key,
                    value=value,
                )

            # Create game configs
            for config_key, value in game_table.config.game_config.to_dict().items():
                _ = GameConfigModel.objects.create(
                    game_table=db_game_table,
                    config_key=config_key,
                    value=value,
                )
        # No GameTablePlayers creation, because there is no players at the moment when table is created

        except Exception as e:
            raise InfrastructureException(detail=f"Could not create game table: {e}") from e

        return game_table.id

    @override
    @transaction.atomic
    def modify_during_game_action(
        self, table_id: str, modifier: Callable[[GameTable], Sequence[GameEvent]]
    ) -> tuple[Sequence[GameEvent], GameTable]:
        try:
            db_game_table = GameTableModel.objects.select_for_update().get(id=table_id)
            game_table = GameTableDeserializer.deserialize_table(db_game_table.snapshot)

            events = modifier(game_table)  # mutates game_table and returns sequence of game events

            # appending events logic
            rows = []

            for event in events:
                rows.append(
                    GameEventModel(game_table=db_game_table, sequence_number=event.seq_number, data=event.to_dict())
                )

            _ = GameEventModel.objects.bulk_create(rows)

            db_game_table.snapshot = game_table.to_dict()
            db_game_table.status = game_table.status.value
            db_game_table.updated_at = timezone.now()
            db_game_table.save(update_fields=["snapshot", "status", "updated_at"])

            return events, game_table

        except GameTableModel.DoesNotExist:
            raise NotExistException(reason="game_table_not_exist")

    @override
    @transaction.atomic
    def modify(self, table_id: str, modifier: Callable[[GameTable], None]) -> GameTable:
        try:
            db_game_table = GameTableModel.objects.select_for_update().get(id=table_id)
            game_table = GameTableDeserializer.deserialize_table(db_game_table.snapshot)

            modifier(game_table)  # mutates game_table

            # deletes all players from the table and reinserts new ones
            _ = PlayerModel.objects.filter(game_table_id=game_table.id).delete()
            for player in game_table.players:
                _ = PlayerModel.objects.create(
                    game_table_id=game_table.id,
                    user_id=player.user_id,
                    screen_name=player.screen_name,
                    bot_strategy_kind=player.bot_strategy.kind.value if player.bot_strategy else None,
                )

            # configs do not change during the game_table's life cycle, so we do not need to update them

            db_game_table.snapshot = game_table.to_dict()
            db_game_table.status = game_table.status.value
            db_game_table.updated_at = timezone.now()
            db_game_table.save(update_fields=["snapshot", "status", "updated_at"])

            return game_table

        except GameTableModel.DoesNotExist:
            raise NotExistException(reason="game_table_not_exist")

    @override
    def delete(self, id: str) -> None:
        try:
            _ = GameTableModel.objects.filter(id=id).delete()
        except GameTableModel.DoesNotExist:
            # table already deleted
            return None

    @override
    def find_by_id(self, id: str) -> GameTable:
        try:
            db_game_table = GameTableModel.objects.get(id=id)
        except GameTableModel.DoesNotExist:
            raise NotExistException(reason="game_table_not_exist")
        except Exception as e:
            raise InfrastructureException(detail=f"Could not find game table by id: {e}") from e
        return GameTableDeserializer.deserialize_table(db_game_table.snapshot)

    @override
    def find_many(self, filters: dict[str, set[str]]) -> QuerySet[GameTableModel]:
        try:
            query_set = (
                GameTableModel.objects.select_related("owner")
                .prefetch_related("players", "game_configs", "table_configs")
                .order_by("-created_at")
            )

            # apply filters
            if "status" in filters and filters["status"]:
                query_set = query_set.filter(status__in=filters["status"])
            if "game_name" in filters and filters["game_name"]:
                query_set = query_set.filter(game_name__in=filters["game_name"])
            return query_set.all()
        except Exception as e:
            raise InfrastructureException(detail=f"Could not find game tables by filters: {e}") from e

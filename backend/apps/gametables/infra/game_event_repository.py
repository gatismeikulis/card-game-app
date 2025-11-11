from typing import override

from django.db.models import QuerySet

from core.exceptions.not_exist_exception import NotExistException
from core.exceptions.infrastructure_exception import InfrastructureException
from ..application.igame_event_repository import IGameEventRepository
from ..models import GameEventModel


class GameEventRepository(IGameEventRepository):
    @override
    def find_many(
        self, table_id: str, start_inclusive: int | None = None, end_inclusive: int | None = None
    ) -> QuerySet[GameEventModel]:
        try:
            query_set = GameEventModel.objects.filter(game_table_id=table_id)

            if start_inclusive is not None:
                query_set = query_set.filter(sequence_number__gte=start_inclusive)
            if end_inclusive is not None:
                query_set = query_set.filter(sequence_number__lte=end_inclusive)
            return query_set

        except GameEventModel.DoesNotExist:
            raise NotExistException(reason="game_event_not_exist")
        except Exception as e:
            raise InfrastructureException(detail=f"Could not find game events: {e}") from e

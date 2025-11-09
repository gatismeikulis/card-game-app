from collections.abc import Sequence
from typing import override

from core.exceptions.not_exist_exception import NotExistException
from core.exceptions.infrastructure_exception import InfrastructureException
from ..application.igame_play_event_repository import IGameEventRepository
from ..models import GameEventModel, GameTableModel
from ..registries.game_event_parsers import get_game_event_parser
from game.game_name import GameName
from game.common.game_event import GameEvent


class GameEventRepository(IGameEventRepository):
    @override
    def find_many(
        self, table_id: str, start_inclusive: int | None = None, end_inclusive: int | None = None
    ) -> Sequence[GameEvent]:
        try:
            db_game_table = GameTableModel.objects.get(pk=table_id)

            query_set = GameEventModel.objects.filter(game_table_id=table_id)

            if start_inclusive is not None:
                query_set = query_set.filter(sequence_number__gte=start_inclusive)
            if end_inclusive is not None:
                query_set = query_set.filter(sequence_number__lte=end_inclusive)

            raw_events = list(query_set.order_by("sequence_number"))

        except GameTableModel.DoesNotExist:
            raise NotExistException(reason="game_table_not_exist")
        except Exception as e:
            raise InfrastructureException(detail=f"Could not find game events: {e}") from e

        game_name = GameName.from_str(db_game_table.game_name)
        parser = get_game_event_parser(game_name)

        return [parser.from_dict(event.data) for event in raw_events]

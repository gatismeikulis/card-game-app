from collections.abc import Sequence
from typing import override
from django.db import transaction
from django.db.models import Max

from core.exceptions.not_exist_exception import NotExistException
from core.exceptions.infrastructure_exception import InfrastructureException
from ..application.igame_play_event_repository import IGamePlayEventRepository
from ..models import GamePlayEvent, GameTableSnapshot
from ..registries.game_event_parsers import get_game_event_parser
from game.game_name import GameName
from game.common.game_event import GameEvent


class GamePlayEventRepository(IGamePlayEventRepository):
    @transaction.atomic
    @override
    def append(self, table_id: str, game_events: Sequence[GameEvent]) -> int:
        try:
            snapshot = GameTableSnapshot.objects.get(pk=table_id)

            max_seq = (
                GamePlayEvent.objects.filter(game_table=snapshot).aggregate(max=Max("sequence_number"))["max"] or 0
            )

            rows = []
            last_sequence_number = max_seq
            for i, event in enumerate(game_events, start=max_seq + 1):
                _ = rows.append(GamePlayEvent(game_table=snapshot, sequence_number=i, data=event.to_dict()))
                last_sequence_number = i

            _ = GamePlayEvent.objects.bulk_create(rows)
            return last_sequence_number
        except GameTableSnapshot.DoesNotExist:
            raise NotExistException(reason="game_table_not_exist")
        except Exception as e:
            raise InfrastructureException(message=f"Could not append game events: {e}") from e

    @override
    def find_many(
        self, table_id: str, start_inclusive: int | None = None, end_inclusive: int | None = None
    ) -> Sequence[GameEvent]:
        try:
            snapshot = GameTableSnapshot.objects.get(pk=table_id)

            query_set = GamePlayEvent.objects.filter(game_table_id=table_id)

            if start_inclusive is not None:
                query_set = query_set.filter(sequence_number__gte=start_inclusive)
            if end_inclusive is not None:
                query_set = query_set.filter(sequence_number__lte=end_inclusive)

            raw_events = list(query_set.order_by("sequence_number"))

        except GameTableSnapshot.DoesNotExist:
            raise NotExistException(reason="game_table_not_exist")
        except Exception as e:
            raise InfrastructureException(message=f"Could not find game events: {e}") from e

        game_name = GameName.from_str(snapshot.game_name)
        parser = get_game_event_parser(game_name)

        return [parser.from_dict(event.data) for event in raw_events]

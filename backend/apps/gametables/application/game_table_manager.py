from collections.abc import Sequence
from typing import Any, final
import uuid
from django.db import transaction

from ..domain.table_status import TableStatus
from .igame_play_event_repository import IGamePlayEventRepository
from .igame_table_repository import IGameTableRepository
from ..models import GameTableSnapshot
from ..registries.table_config_parsers import get_table_config_parser
from ..registries.game_config_parsers import get_game_config_parser
from ..registries.bot_strategies import get_bot_strategy
from ..registries.game_command_parsers import get_command_parser
from ..registries.game_engines import get_game_engine
from apps.users.models import User
from game.bot_strategy_kind import BotStrategyKind
from game.common.game_event import GameEvent
from game.common.seat import SeatNumber
from game.game_name import GameName
from ..domain.game_table import GameTable
from ..domain.game_table_config import GameTableConfig


@final
class GameTableManager:
    def __init__(
        self,
        game_table_repository: IGameTableRepository,
        game_play_event_repository: IGamePlayEventRepository,
    ) -> None:
        self._game_table_repository: IGameTableRepository = game_table_repository
        self._game_play_event_repository: IGamePlayEventRepository = game_play_event_repository

    def _generate_table_id(self) -> str:
        return str(uuid.uuid4())

    def _validate_user_is_owner_of_table(self, table: GameTable, user_id: int) -> None:
        if table.owner_id != user_id:
            raise ValueError("Only table owner can perform this action")

    def add_table(self, raw_config: dict[str, Any], owner_id: int) -> str:
        table_id = self._generate_table_id()
        game_name = GameName.from_str(raw_config["game_name"])
        game_config = get_game_config_parser(game_name).from_dict(raw_config.get("game_config", {}))
        table_config = get_table_config_parser(game_name).from_dict(raw_config.get("table_config", {}))
        config = GameTableConfig(game_name, game_config, table_config)
        engine = get_game_engine(config.game_name)
        table = GameTable(table_id=table_id, config=config, engine=engine, owner_id=owner_id)
        table_id = self._game_table_repository.create(table)
        return table_id

    def remove_table(self, table_id: str, iniated_by: int) -> None:
        table = self._game_table_repository.find_by_id(table_id)
        self._validate_user_is_owner_of_table(table, iniated_by)
        if table.status == TableStatus.NOT_STARTED:
            _ = self._game_table_repository.delete(table_id)
        else:
            table.cancel_game()
            self._game_table_repository.update(table)
        return None

    def get_tables(self) -> Sequence[GameTableSnapshot]:
        return self._game_table_repository.find_many()

    def get_table(self, table_id: str) -> GameTable:
        return self._game_table_repository.find_by_id(table_id)

    def join_table(self, table_id: str, user: User, preferred_seat_number: SeatNumber | None = None) -> str:
        table = self._game_table_repository.find_by_id(table_id)
        table.add_player(
            user_id=user.pk,
            screen_name=user.screen_name,
            preferred_seat_number=preferred_seat_number,
        )
        self._game_table_repository.update(table)
        return table_id

    def leave_table(self, table_id: str, user_id: int) -> None:
        table = self._game_table_repository.find_by_id(table_id)
        table.remove_player(user_id=user_id)
        self._game_table_repository.update(table)
        return None

    def add_bot_player(
        self,
        table_id: str,
        iniated_by: User,
        options: dict[str, Any],
    ) -> None:
        bot_strategy_kind = BotStrategyKind.from_str(options["bot_strategy_kind"])
        preferred_seat_number = options.get("preferred_seat", None)
        table = self._game_table_repository.find_by_id(table_id)
        self._validate_user_is_owner_of_table(table, iniated_by.pk)
        bot_strategy = get_bot_strategy(table.config.game_name, bot_strategy_kind)
        table.add_player(preferred_seat_number=preferred_seat_number, bot_strategy=bot_strategy)
        self._game_table_repository.update(table)
        return None

    def remove_bot_player(self, table_id: str, iniated_by: int, seat_number_to_remove: SeatNumber) -> None:
        table = self._game_table_repository.find_by_id(table_id)
        self._validate_user_is_owner_of_table(table, iniated_by)
        table.remove_player(seat_number=seat_number_to_remove)
        self._game_table_repository.update(table)
        return None

    def start_game(self, table_id: str, iniated_by: int) -> None:
        table = self._game_table_repository.find_by_id(table_id)
        self._validate_user_is_owner_of_table(table, iniated_by)
        events = table.start_game()
        return self._complete_game_action(table, events)

    def take_regular_turn(self, table_id: str, user_id: int, raw_command: dict[str, Any]) -> None:
        table = self._game_table_repository.find_by_id(table_id)
        command = get_command_parser(table.config.game_name).from_dict(raw_command)
        events = table.take_regular_turn(user_id=user_id, command=command)
        return self._complete_game_action(table, events)

    def take_automatic_turn(self, table_id: str, iniated_by: int) -> None:
        table = self._game_table_repository.find_by_id(table_id)
        self._validate_user_is_owner_of_table(table, iniated_by)
        events = table.take_automatic_turn()
        return self._complete_game_action(table, events)

    @transaction.atomic
    def _complete_game_action(self, table: GameTable, events: Sequence[GameEvent]) -> None:
        if events:
            last_sequence_number = self._game_play_event_repository.append(table.id, events)
            self._game_table_repository.update_after_game_action(table, last_sequence_number)

        return None

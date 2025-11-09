from collections.abc import Sequence
from typing import Any, final
import uuid

from core.exceptions.app_exception import AppException
from .igame_event_repository import IGameEventRepository
from .igame_table_repository import IGameTableRepository
from ..exceptions import GameTableInternalException
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
        game_play_event_repository: IGameEventRepository,
    ) -> None:
        self._game_table_repository: IGameTableRepository = game_table_repository
        self._game_play_event_repository: IGameEventRepository = game_play_event_repository

    def _generate_table_id(self) -> str:
        return str(uuid.uuid4())

    def add_table(self, raw_config: dict[str, Any], owner_id: int) -> str:
        try:
            table_id = self._generate_table_id()
            game_name = GameName.from_str(raw_config["game_name"])
            game_config = get_game_config_parser(game_name)(raw_config.get("game_config", {}))
            table_config = get_table_config_parser(game_name)(raw_config.get("table_config", {}))
            config = GameTableConfig(game_name, game_config, table_config)
            engine = get_game_engine(config.game_name)
            table = GameTable(table_id=table_id, config=config, engine=engine, owner_id=owner_id)
            table_id = self._game_table_repository.create(table)
            return table_id
        except AppException as e:
            raise e.with_context(user_id=owner_id, operation="add_table")

    def remove_table(self, table_id: str, iniated_by: int) -> None:
        try:
            table = self._game_table_repository.find_by_id(table_id)
            if table.can_remove(iniated_by):
                self._game_table_repository.delete(table_id)
        except AppException as e:
            raise e.with_context(table_id=table_id, operation="remove_table")

    def get_table(self, table_id: str) -> GameTable:
        try:
            return self._game_table_repository.find_by_id(table_id)
        except AppException as e:
            raise e.with_context(table_id=table_id, operation="get_table")

    def join_table(self, table_id: str, user: User, preferred_seat_number: SeatNumber | None = None) -> GameTable:
        try:

            def _modifier(table: GameTable) -> None:
                table.add_human_player(
                    user_id=user.pk,
                    screen_name=user.screen_name,
                    preferred_seat_number=preferred_seat_number,
                )

            return self._game_table_repository.modify(table_id, _modifier)
        except AppException as e:
            raise e.with_context(table_id=table_id, user_id=user.pk, operation="join_table")

    def leave_table(self, table_id: str, user_id: int) -> GameTable:
        try:

            def _modifier(table: GameTable) -> None:
                table.remove_human_player(user_id=user_id)

            return self._game_table_repository.modify(table_id, _modifier)
        except AppException as e:
            raise e.with_context(table_id=table_id, user_id=user_id, operation="leave_table")

    def add_bot_player(
        self,
        table_id: str,
        iniated_by: int,
        options: dict[str, Any],
    ) -> GameTable:
        try:

            def _modifier(table: GameTable) -> None:
                bot_strategy_kind = BotStrategyKind.from_str(options["bot_strategy_kind"])
                preferred_seat_number = options.get("preferred_seat", None)
                bot_strategy = get_bot_strategy(table.config.game_name, bot_strategy_kind)
                table.add_bot_player(
                    bot_strategy=bot_strategy, initiated_by=iniated_by, preferred_seat_number=preferred_seat_number
                )

            return self._game_table_repository.modify(table_id, _modifier)
        except AppException as e:
            raise e.with_context(table_id=table_id, user_id=iniated_by, operation="add_bot_player")

    def remove_bot_player(self, table_id: str, iniated_by: int, seat_number_to_remove: SeatNumber) -> GameTable:
        try:

            def _modifier(table: GameTable) -> None:
                table.remove_bot_player(seat_number=seat_number_to_remove, initiated_by=iniated_by)

            return self._game_table_repository.modify(table_id, _modifier)
        except AppException as e:
            raise e.with_context(table_id=table_id, user_id=iniated_by, operation="remove_bot_player")

    def start_game(self, table_id: str, iniated_by: int) -> tuple[Sequence[GameEvent], GameTable]:
        try:

            def _modifier(table: GameTable) -> Sequence[GameEvent]:
                return table.start_game(initiated_by=iniated_by)

            return self._game_table_repository.modify_during_game_action(table_id, _modifier)
        except AppException as e:
            raise e.with_context(table_id=table_id, user_id=iniated_by, operation="start_game")

    def take_regular_turn(
        self, table_id: str, user_id: int, raw_command: dict[str, Any]
    ) -> tuple[Sequence[GameEvent], GameTable]:
        try:

            def _modifier(table: GameTable) -> Sequence[GameEvent]:
                command = get_command_parser(table.config.game_name).from_dict(raw_command)
                return table.take_regular_turn(user_id=user_id, command=command)

            return self._game_table_repository.modify_during_game_action(table_id, _modifier)
        except AppException as e:
            raise e.with_context(table_id=table_id, user_id=user_id, operation="take_regular_turn")

    def take_automatic_turn(self, table_id: str, initiated_by: int) -> tuple[Sequence[GameEvent], GameTable]:
        try:

            def _modifier(table: GameTable) -> Sequence[GameEvent]:
                return table.take_automatic_turn(initiated_by=initiated_by)

            return self._game_table_repository.modify_during_game_action(table_id, _modifier)
        except AppException as e:
            raise e.with_context(table_id=table_id, user_id=initiated_by, operation="take_automatic_turn")

    def cancel_game(
        self, table_id: str, initiated_by: int, raw_command: dict[str, Any]
    ) -> tuple[Sequence[GameEvent], GameTable]:
        try:

            def _modifier(table: GameTable) -> Sequence[GameEvent]:
                command = get_command_parser(table.config.game_name).from_dict(raw_command)
                return table.cancel_game(initiated_by=initiated_by, command=command)

            return self._game_table_repository.modify_during_game_action(table_id, _modifier)
        except AppException as e:
            raise e.with_context(table_id=table_id, user_id=initiated_by, operation="cancel_game")

    def abort_game(
        self, table_id: str, initiated_by: int, to_blame: int, raw_command: dict[str, Any]
    ) -> tuple[Sequence[GameEvent], GameTable]:
        try:

            def _modifier(table: GameTable) -> Sequence[GameEvent]:
                command = get_command_parser(table.config.game_name).from_dict(raw_command)
                return table.abort_game(initiated_by=initiated_by, to_blame=to_blame, command=command)

            return self._game_table_repository.modify_during_game_action(table_id, _modifier)
        except AppException as e:
            raise e.with_context(table_id=table_id, user_id=initiated_by, operation="abort_game")

    def get_table_from_past(self, table_id: str, upto_event: int) -> GameTable:
        try:
            table = self._game_table_repository.find_by_id(table_id)
            events = self._game_play_event_repository.find_many(table_id, end_inclusive=upto_event)
            if not events:
                raise GameTableInternalException(detail="Could not get table from past: no history availble")
            table.restore_game_state(events)
            return table
        except AppException as e:
            raise e.with_context(table_id=table_id, upto_event=upto_event, operation="get_table_from_past")

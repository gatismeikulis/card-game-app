from collections.abc import Mapping, Sequence
from typing import Any, final
import uuid
import logging

from core.exceptions.infrastructure_exception import InfrastructureException
from core.exceptions.app_exception import AppException
from .igame_event_repository import IGameEventRepository
from .igame_table_repository import IGameTableRepository
from .igame_state_snapshot_repository import IGameStateSnapshotRepository
from ..registries.table_config_parsers import get_table_config_parser
from ..registries.game_config_parsers import get_game_config_parser
from ..registries.bot_strategies import get_bot_strategy
from ..registries.game_command_parsers import get_command_parser
from ..registries.game_engines import get_game_engine
from ..registries.game_classes import get_game_class
from ..registries.game_event_parsers import get_game_event_parser
from apps.users.models import User
from game.bot_strategy_kind import BotStrategyKind
from game.common.game_event import GameEvent
from game.common.seat import SeatNumber
from game.game_name import GameName
from game.common.game_state import GameState
from ..domain.game_table import GameTable
from ..domain.game_table_config import GameTableConfig

logger = logging.getLogger(__name__)


@final
class GameTableManager:
    def __init__(
        self,
        game_table_repository: IGameTableRepository,
        game_event_repository: IGameEventRepository,
        game_state_snapshot_repository: IGameStateSnapshotRepository,
    ) -> None:
        self._game_table_repository: IGameTableRepository = game_table_repository
        self._game_event_repository: IGameEventRepository = game_event_repository
        self._game_state_snapshot_repository: IGameStateSnapshotRepository = game_state_snapshot_repository

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

    def remove_table(self, table_id: str, initiated_by: int) -> None:
        try:
            table = self._game_table_repository.find_by_id(table_id)
            if table.can_remove(initiated_by):
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
        initiated_by: int,
        options: dict[str, Any],
    ) -> GameTable:
        try:

            def _modifier(table: GameTable) -> None:
                bot_strategy_kind = BotStrategyKind.from_str(options["bot_strategy_kind"])
                preferred_seat_number = options.get("preferred_seat", None)
                bot_strategy = get_bot_strategy(table.config.game_name, bot_strategy_kind)
                table.add_bot_player(
                    bot_strategy=bot_strategy, initiated_by=initiated_by, preferred_seat_number=preferred_seat_number
                )

            return self._game_table_repository.modify(table_id, _modifier)
        except AppException as e:
            raise e.with_context(table_id=table_id, user_id=initiated_by, operation="add_bot_player")

    def remove_bot_player(self, table_id: str, initiated_by: int, seat_number_to_remove: SeatNumber) -> GameTable:
        try:

            def _modifier(table: GameTable) -> None:
                table.remove_bot_player(seat_number=seat_number_to_remove, initiated_by=initiated_by)

            return self._game_table_repository.modify(table_id, _modifier)
        except AppException as e:
            raise e.with_context(table_id=table_id, user_id=initiated_by, operation="remove_bot_player")

    def start_game(self, table_id: str, initiated_by: int) -> tuple[Sequence[GameEvent], GameTable]:
        try:

            def _modifier(table: GameTable) -> Sequence[GameEvent]:
                return table.start_game(initiated_by=initiated_by)

            return self._game_table_repository.modify_during_game_action(table_id, _modifier)
        except AppException as e:
            raise e.with_context(table_id=table_id, user_id=initiated_by, operation="start_game")

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

    def get_game_state_snapshot(self, table_id: str, event_number: int) -> Mapping[str, Any]:
        try:
            data = self._game_state_snapshot_repository.get_exact_or_nearest_snapshot_data(table_id, event_number)

            if data and data["is_exact"]:
                logger.info(f"Exact snapshot found for table {table_id} and event number {event_number}")
                return data["snapshot"]

            table = self._game_table_repository.find_by_id(table_id)

            if table.replay_safe_game_event_number < event_number:
                raise AppException(
                    detail="Event number is greater than the replay safe event number", reason="event_number_too_large"
                )

            return self.create_and_store_game_state_snapshots(
                table, raw_initial_game_state=data["snapshot"] if data else None, up_to_event_number=event_number
            )

        except AppException as e:
            raise e.with_context(table_id=table_id, event_number=event_number, operation="get_game_state_snapshot")

    def create_and_store_game_state_snapshots(
        self, table: GameTable, raw_initial_game_state: dict[str, Any] | None, up_to_event_number: int | None
    ) -> Mapping[str, Any]:
        try:
            raw_game_state: dict[str, Any] | None = raw_initial_game_state
            game_state: GameState | None = None
            start_event_number: int | None = raw_game_state["event_number"] + 1 if raw_game_state else None

            logger.info(
                f"Creating and storing game state snapshots for table {table.id} from event number {start_event_number or 0} up to event number {up_to_event_number}"
            )

            db_events = self._game_event_repository.find_many(table.id, start_event_number, up_to_event_number)

            if raw_game_state:
                game_state = get_game_class(table.config.game_name).from_dict(raw_game_state)

            data_to_store: list[dict[str, Any]] = []

            game_event_parser = get_game_event_parser(table.config.game_name)

            if not game_state:
                game_state = table.get_initial_or_after_event_game_state(None, None)
                raw_game_state = game_state.to_dict()
                data_to_store.append(raw_game_state)

            db_events = self._game_event_repository.find_many(table.id, start_event_number, up_to_event_number)

            for db_event in db_events:
                event = game_event_parser.from_dict(db_event.data)
                game_state = table.get_initial_or_after_event_game_state(game_state=game_state, event_to_apply=event)
                raw_game_state = game_state.to_dict()

                if raw_game_state["event_number"] != event.seq_number:
                    logger.error(f"Event number mismatch: {raw_game_state['event_number']} != {event.seq_number}")
                    raise InfrastructureException(detail="Event number mismatch", reason="event_number_mismatch")

                data_to_store.append(raw_game_state)

            self._game_state_snapshot_repository.store(table.id, data_to_store)

            if not raw_game_state:
                raise AppException(detail="Could not restore game state from events", reason="game_state_not_restored")

            return raw_game_state

        except AppException as e:
            raise e.with_context(table_id=table.id, operation="create_and_store_game_state_snapshots")

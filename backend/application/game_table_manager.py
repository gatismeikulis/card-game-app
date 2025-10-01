from collections.abc import Sequence
from typing import Any, final

from backend.application.bot_strategy_registry import BotStrategyRegistry
from backend.application.game_command_parsing_service import GameCommandParsingService
from backend.domain.core.user_id import UserId
from backend.domain.game.bot_strategy_kind import BotStrategyKind
from backend.domain.game.common.game_event import GameEvent
from backend.domain.game.common.seat import SeatNumber
from backend.domain.lobby.lobby import Lobby
from backend.domain.table.game_table import GameTable
from backend.domain.table.game_table_config import GameTableConfig
from backend.domain.table.table_id import TableId


@final
class GameTableManager:
    def __init__(
        self,
        lobby: Lobby,
        game_command_parsing_service: GameCommandParsingService,
        bot_strategy_registry: BotStrategyRegistry,
    ) -> None:
        self._lobby: Lobby = lobby
        self._game_command_parsing_service: GameCommandParsingService = game_command_parsing_service
        self._bot_strategy_registry: BotStrategyRegistry = bot_strategy_registry

    # Lobby related methods

    def add_table(self, config: GameTableConfig) -> None:
        self._lobby.add_table(config)

    def remove_table(self, table_id: TableId) -> None:
        self._lobby.remove_table(table_id)

    def get_tables(self) -> Sequence[GameTable]:
        return self._lobby.get_tables()

    # Table related methods

    def join_table(self, table_id: TableId, user_id: UserId, preferred_seat_number: SeatNumber | None = None) -> None:
        self._lobby.table_by_id(table_id).add_player(user_id, preferred_seat_number)

    def add_bot_player(
        self,
        table_id: TableId,
        user_id: UserId,
        bot_strategy_kind: BotStrategyKind,
        preferred_seat_number: SeatNumber | None = None,
    ) -> None:
        table = self._lobby.table_by_id(table_id)
        bot_strategy = self._bot_strategy_registry.get(table.config.game_name, bot_strategy_kind)
        table.add_player(user_id, preferred_seat_number, bot_strategy=bot_strategy)

    def leave_table(self, table_id: TableId, user_id: UserId) -> None:
        self._lobby.table_by_id(table_id).remove_player(user_id)

    def start_game(self, table_id: TableId, iniated_by: UserId) -> None:
        self._lobby.table_by_id(table_id).start_game(iniated_by)

    def take_regular_turn(self, table_id: TableId, user_id: UserId, raw_command: dict[str, Any]) -> Sequence[GameEvent]:
        table = self._lobby.table_by_id(table_id)
        command = self._game_command_parsing_service.parse(table.config.game_name, raw_command)
        return table.take_regular_turn(user_id, command)

    def take_automatic_turn(self, table_id: TableId, bot_id: UserId) -> Sequence[GameEvent]:
        return self._lobby.table_by_id(table_id).take_automatic_turn(bot_id)

from typing import Any, final

from backend.application.game_command_factory import GameCommandFactory
from backend.domain.core.user_id import UserId
from backend.domain.game.common.seat import SeatNumber
from backend.domain.game.game_name import GameName
from backend.domain.lobby.lobby import Lobby
from backend.domain.table.game_table import GameTable
from backend.domain.table.game_table_config import GameTableConfig
from backend.domain.table.table_id import TableId


@final
class GameTableManager:
    # TODO add dependency injection for lobby (repos, event-store, notification-service, etc)
    def __init__(self, lobby: Lobby, game_command_factory: GameCommandFactory) -> None:
        self._lobby: Lobby = lobby
        self._game_command_factory: GameCommandFactory = game_command_factory

    # Lobby related methods

    def add_table(self, game_name: GameName, config: GameTableConfig) -> None:
        self._lobby.add_table(game_name, config)  #

    def remove_table(self, table_id: TableId) -> None:
        self._lobby.remove_table(table_id)

    def get_tables(self) -> list[GameTable[Any, Any, Any]]:
        return self._lobby.get_tables()

    # Table related methods

    def join_table(self, table_id: TableId, user_id: UserId, seat_number: SeatNumber | None = None) -> None:
        self._lobby.table_by_id(table_id).add_player(user_id, seat_number)

    def leave_table(self, table_id: TableId, user_id: UserId) -> None:
        self._lobby.table_by_id(table_id).remove_player(user_id)

    def start_game(self, table_id: TableId, iniated_by: UserId) -> None:
        self._lobby.table_by_id(table_id).start_game(iniated_by)

    def play_turn(self, table_id: TableId, user_id: UserId, raw_command: dict[str, Any] | None = None) -> None:
        table = self._lobby.table_by_id(table_id)
        if raw_command is None:
            command = None
        else:
            command = self._game_command_factory.create(table.config.game_name, raw_command)
        self._lobby.table_by_id(table_id).play_turn(user_id, command)

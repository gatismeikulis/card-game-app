from typing import Generic, TypeVar, override

from backend.domain.core.user_id import UserId
from backend.domain.game.common.command import Command
from backend.domain.game.common.event import Event
from backend.domain.game.common.game_engine import GameEngine
from backend.domain.game.common.game_state import GameState
from backend.domain.game.common.seat import Seat
from backend.domain.table.game_table_config import GameTableConfig
from backend.domain.table.table_id import TableId

TCommand = TypeVar("TCommand", bound=Command)
TEvent = TypeVar("TEvent", bound=Event)
TSeat = TypeVar("TSeat", bound=Seat)
TGameState = TypeVar("TGameState", bound=GameState)


class GameTable(Generic[TGameState, TCommand, TEvent, TSeat]):
    def __init__(self, table_id: TableId, config: GameTableConfig, engine: GameEngine[TGameState, TCommand, TEvent]):
        self._id: TableId = table_id
        self._config: GameTableConfig = config
        self._players: dict[UserId, TSeat] = {}  # change to user_id -> game_seat
        self._game_state: TGameState | None = None
        self._spectators: set[UserId] = set()  # change to user_id
        self._engine: GameEngine[TGameState, TCommand, TEvent] = engine

    @property
    def config(self) -> GameTableConfig:
        return self._config

    @property
    def players(self) -> dict[UserId, TSeat]:
        return self._players

    @property
    def spectators(self) -> set[UserId]:
        return self._spectators

    @property
    def id(self) -> TableId:
        return self._id

    @property
    def game_state(self) -> TGameState:
        if self._game_state is None:
            raise ValueError("Game state is not initialized")
        return self._game_state

    # this command should update game state and return events so they can be persisted in layer above
    def process_command(self, user_id: UserId, command: TCommand) -> list[TEvent]:
        game_state = self._game_state
        if game_state is None:
            raise ValueError("Game state is not initialized")
        if game_state.active_seat != self._players[user_id]:
            raise ValueError("Not the player's turn")
        game_state_updated, events = self._engine.process_command(game_state, command)
        self._game_state = game_state_updated
        return events

    def add_player(self, user_id: UserId, seat: TSeat) -> None:
        if len(self._players) >= self._config.max_players:
            raise ValueError("Table is full")
        if user_id in self._players.keys():
            raise ValueError("Player already exists at this table")
        if seat in self._players.values():
            raise ValueError("Seat already taken")
        self._players[user_id] = seat

    def remove_player(self, user_id: UserId) -> None:
        # not allowed to leave if game is started
        # should end the game before leaving
        del self._players[user_id]

    def start_game(self) -> None:
        if len(self._players) < self._config.min_players:
            raise ValueError("Not enough players to start the game")
        self._game_state = self._engine.init_game()

    @override
    def __str__(self) -> str:
        return f"""Table {self._id} with {len(self._players)} players and {len(self._spectators)} spectators:
        Players: {self._players}
        Spectators: {self._spectators}
        Game state: {self._game_state}
        """

    @override
    def __repr__(self) -> str:
        return self.__str__()

import random
from collections.abc import Mapping, Sequence
from typing import override

from backend.domain.core.user_id import UserId
from backend.domain.game.common.bot_strategy import BotStrategy
from backend.domain.game.common.game_command import GameCommand
from backend.domain.game.common.game_engine import GameEngine
from backend.domain.game.common.game_event import GameEvent
from backend.domain.game.common.game_state import GameState
from backend.domain.game.common.seat import SeatNumber
from backend.domain.table.game_table_config import GameTableConfig
from backend.domain.table.player import Player
from backend.domain.table.table_id import TableId


class GameTable:
    def __init__(self, table_id: TableId, config: GameTableConfig, engine: GameEngine):
        self._id: TableId = table_id
        self._config: GameTableConfig = config
        self._players: dict[UserId, Player] = {}
        self._game_state: GameState | None = None
        self._engine: GameEngine = engine

    @property
    def config(self) -> GameTableConfig:
        return self._config

    @property
    def players(self) -> Mapping[UserId, Player]:
        return self._players

    @property
    def id(self) -> TableId:
        return self._id

    @property
    def game_state(self) -> GameState:
        if self._game_state is None:
            raise ValueError("Game state is not initialized")
        return self._game_state

    # regular turn is a turn taken by a human player by providing a command
    def take_regular_turn(self, user_id: UserId, command: GameCommand) -> Sequence[GameEvent]:
        game_state = self._validate_can_take_turn(user_id)
        return self._take_turn(game_state, command)

    # automatic turn is a turn taken by a bot player by producing a command
    # this may be async because it may take time to create a command using bot strategy
    def take_automatic_turn(self, user_id: UserId) -> Sequence[GameEvent]:
        game_state = self._validate_can_take_turn(user_id)
        bot_strategy = self._players[user_id].bot_strategy
        if bot_strategy is None:
            raise ValueError(f"Bot strategy is not set for user {user_id}")
        command = bot_strategy.create_command(game_state)
        return self._take_turn(game_state, command)

    def _validate_can_take_turn(self, user_id: UserId) -> GameState:
        game_state = self.game_state
        if game_state.active_seat.number != self._players[user_id].seat_number:
            raise ValueError(f"Not the player's with id {user_id} turn")
        return game_state

    def _take_turn(self, game_state: GameState, command: GameCommand) -> Sequence[GameEvent]:
        game_state_updated, events = self._engine.process_command(game_state, command)
        self._game_state = game_state_updated
        return events

    def add_player(
        self, user_id: UserId, preferred_seat_number: SeatNumber | None = None, bot_strategy: BotStrategy | None = None
    ) -> None:
        if len(self._players) >= self._config.max_players:
            raise ValueError(f"Table {self._id} is full")
        if user_id in self._players:
            raise ValueError(f"Player with id {user_id} already exists at this table {self._id}")
        taken_seat_numbers = {player.seat_number for player in self.players.values()}
        available_seat_numbers = set(self._config.possible_seat_numbers) - taken_seat_numbers
        # if seat number is not provided, choose random one. if it is provided, use it if it is available
        if preferred_seat_number is not None:
            if preferred_seat_number not in available_seat_numbers:
                raise ValueError(f"Preferred seat number {preferred_seat_number} is not available at table {self._id}")
            available_seat_numbers = {preferred_seat_number}
        seat_number = random.choice(list(available_seat_numbers))
        self._players[user_id] = Player(seat_number, agreed_to_start=False, bot_strategy=bot_strategy)

    def remove_player(self, user_id: UserId) -> None:
        # not allowed to leave if game is started
        # should end the game before leaving
        del self._players[user_id]

    def start_game(self, iniated_by: UserId) -> None:
        # TODO: check if iniated_by is a player at the table. maybe keep track if all players have agreed to start the game
        if len(self._players) < self._config.min_players:
            raise ValueError("Not enough players to start the game")
        self._game_state = self._engine.init_game()

    @override
    def __str__(self) -> str:
        return f"""Table [{self._id}] with {len(self._players)} players:
Players: {[k for k in self.players.keys()]}
{self._game_state}
"""

    @override
    def __repr__(self) -> str:
        return self.__str__()

import random
from collections.abc import Sequence
from typing import Any, override
import uuid

from .table_status import TableStatus
from game.common.bot_strategy import BotStrategy
from game.common.game_command import GameCommand
from game.common.game_engine import GameEngine
from game.common.game_event import GameEvent
from game.common.game_state import GameState
from game.common.seat import SeatNumber
from .game_table_config import GameTableConfig
from .player import Player


class GameTable:
    def __init__(
        self,
        table_id: str,
        config: GameTableConfig,
        engine: GameEngine,
        owner_id: int,
        status: TableStatus = TableStatus.NOT_STARTED,
    ):
        self._id: str = table_id
        self._config: GameTableConfig = config
        self._players: list[Player] = []
        self._owner_id: int = owner_id
        self._game_state: GameState | None = None
        self._engine: GameEngine = engine
        self._status: TableStatus = status

    @property
    def config(self) -> GameTableConfig:
        return self._config

    @property
    def players(self) -> Sequence[Player]:
        return self._players

    @property
    def id(self) -> str:
        return self._id

    @property
    def owner_id(self) -> int:
        return self._owner_id

    @property
    def game_state(self) -> GameState:
        if self._game_state is None:
            raise ValueError("Game state is not initialized")
        return self._game_state

    @property
    def active_player(self) -> Player:
        player = next(
            (player for player in self._players if player.seat_number == self.game_state.active_seat.number), None
        )
        if player is None:
            raise ValueError(f"Player with seat number {self.game_state.active_seat.number} not found")
        return player

    @property
    def status(self) -> TableStatus:
        return self._status

    # regular turn is a turn taken by a human player by providing a command
    def take_regular_turn(self, user_id: int, command: GameCommand) -> Sequence[GameEvent]:
        if self.active_player.user_id != user_id:
            raise ValueError(f"Not the player's with id {user_id} turn")
        return self._take_turn(self.game_state, command)

    # automatic turn is a turn taken by a bot player by producing a command
    # this may be async because it may take time to create a command using bot strategy
    def take_automatic_turn(self) -> Sequence[GameEvent]:
        active_player = self.active_player
        if not active_player.is_bot:
            raise ValueError("Not a bot's turn")
        bot_strategy = active_player.bot_strategy
        if bot_strategy is None:
            raise ValueError(f"Bot strategy is not set for {active_player.screen_name} ({active_player.player_id})")
        game_state = self.game_state
        command = bot_strategy.create_command(game_state)
        return self._take_turn(game_state, command)

    def _take_turn(self, game_state: GameState, command: GameCommand) -> Sequence[GameEvent]:
        game_state_updated, events = self._engine.process_command(game_state, command)
        self._status = TableStatus.IN_PROGRESS
        if game_state_updated.is_finished:
            self._status = TableStatus.FINISHED
        self._game_state = game_state_updated
        return events

    def _generate_seat_number(self, choices: set[SeatNumber]) -> SeatNumber:
        return random.choice(list(choices))

    def _generate_bot_player_id(self) -> str:
        return "bot-" + str(uuid.uuid4())

    def add_player(
        self,
        user_id: int | None = None,
        screen_name: str | None = None,
        preferred_seat_number: SeatNumber | None = None,
        bot_strategy: BotStrategy | None = None,
    ) -> None:
        if len(self._players) >= self._config.game_config.max_seats:
            raise ValueError(f"Table {self._id} is full")
        if user_id is not None and user_id in [player.user_id for player in self._players]:
            raise ValueError(f"Player with id {user_id} already exists at this table {self._id}")
        taken_seat_numbers = {player.seat_number for player in self.players}
        available_seat_numbers = set(self._config.possible_seat_numbers) - taken_seat_numbers
        # if seat number is not provided, choose random one. if it is provided, use it if it is available
        if preferred_seat_number is not None:
            if preferred_seat_number not in available_seat_numbers:
                raise ValueError(f"Preferred seat number {preferred_seat_number} is not available at table {self._id}")
            available_seat_numbers = {preferred_seat_number}
        seat_number = self._generate_seat_number(available_seat_numbers)
        player_id = "human-" + str(user_id) if bot_strategy is None else self._generate_bot_player_id()
        player = Player(
            player_id=player_id,
            seat_number=seat_number,
            screen_name=screen_name if screen_name is not None else f"bot_{seat_number}",
            bot_strategy=bot_strategy,
            user_id=user_id,
        )
        self._players.append(player)

    def remove_player(self, user_id: int | None = None, seat_number: SeatNumber | None = None) -> None:
        if user_id is not None:
            to_remove = next((player for player in self._players if player.user_id == user_id), None)
            if to_remove is None:
                raise ValueError(f"Player with user-id {user_id} not found")
            self._players.remove(to_remove)
        elif seat_number is not None:
            to_remove = next(
                (player for player in self._players if player.seat_number == seat_number),
                None,
            )
            if to_remove is None:
                raise ValueError(f"Player with seat number {seat_number} not found")
            self._players.remove(to_remove)
        else:
            raise ValueError("Either user id or seat number must be provided")

    def start_game(self) -> None:
        # TODO: maybe check if all players have agreed to start
        if len(self._players) < self._config.game_config.min_seats:
            raise ValueError("Not enough players to start the game")
        if self._status != TableStatus.NOT_STARTED:
            raise ValueError("Game already started")
        self._game_state = self._engine.init_game()
        self._status = TableStatus.JUST_STARTED

    def rebuild_game_state(self, events: Sequence[GameEvent]) -> None:
        if len(events) == 0:
            return
        self._game_state = self._engine.rebuild_game_state(self.game_state, events)
        if self._game_state.is_finished:
            self._status = TableStatus.FINISHED
        else:
            self._status = TableStatus.IN_PROGRESS

    def to_dict(self) -> dict[str, Any]:
        """Serialize to JSON-compatible dict"""
        return {
            "id": self._id,
            "config": self._config.to_dict(),
            "players": [player.to_dict() for player in self._players],
            "owner_id": self._owner_id,
            "game_state": self._game_state.to_dict() if self._game_state else None,
            "status": self.status.value,
        }

    def to_public_dict(self, seat_number: SeatNumber | None = None) -> dict[str, Any]:
        return {
            "id": self._id,
            "config": self._config.to_dict(),
            "players": [player.to_dict() for player in self._players],
            "owner_id": self._owner_id,
            "game_state": self._game_state.to_public_dict(seat_number) if self._game_state else None,
            "status": self.status.value,
        }

    @override
    def __str__(self) -> str:
        return f"""Table [{self._id}] with {len(self._players)} players:
{"\n".join(f"-{player.seat_number}- {player.screen_name} [{player.player_id}]" for player in self._players)}
{self._game_state.str_repr_for_table() if self._game_state else "Game not started yet"}
"""

    @override
    def __repr__(self) -> str:
        return self.__str__()

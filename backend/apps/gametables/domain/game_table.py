import random
from collections.abc import Sequence
from typing import Any, override
import uuid

from ..exceptions import GameTableInternalException, GameTableRulesException
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
            raise GameTableInternalException(detail="Could not access game state: game state is not initialized")
        return self._game_state

    @property
    def active_player(self) -> Player:
        player = next(
            (player for player in self._players if player.seat_number == self.game_state.active_seat.number), None
        )
        if player is None:
            raise GameTableInternalException(
                detail=f"Could not access active player: player with seat number {self.game_state.active_seat.number} not found"
            )
        return player

    @property
    def status(self) -> TableStatus:
        return self._status

    @property
    def taken_seat_numbers(self) -> frozenset[SeatNumber]:
        return frozenset({player.seat_number for player in self._players})

    def add_human_player(self, user_id: int, screen_name: str, preferred_seat_number: SeatNumber | None = None) -> None:
        self._validate_status(acceptable_statuses={TableStatus.NOT_STARTED})
        self._validate_has_free_seats()
        self._validate_can_join_table(user_id)
        seat_number = self._get_seat_number(preferred_seat_number)
        player_id = "human-" + str(user_id)
        player = Player(
            player_id=player_id,
            seat_number=seat_number,
            screen_name=screen_name,
            bot_strategy=None,
            user_id=user_id,
        )
        self._players.append(player)

    def add_bot_player(
        self, bot_strategy: BotStrategy, initiated_by: int, preferred_seat_number: SeatNumber | None = None
    ) -> None:
        self._validate_status(acceptable_statuses={TableStatus.NOT_STARTED})
        self._validate_has_free_seats()
        self._validate_is_owner(initiated_by)
        self._validate_bots_allowed()
        seat_number = self._get_seat_number(preferred_seat_number)
        player_id = self._generate_bot_player_id()
        player = Player(
            player_id=player_id,
            seat_number=seat_number,
            screen_name=f"bot_{seat_number}",
            bot_strategy=bot_strategy,
        )
        self._players.append(player)

    def remove_human_player(self, user_id: int) -> None:
        self._validate_status(acceptable_statuses={TableStatus.NOT_STARTED})
        self._validate_is_player(user_id)
        to_remove = next((player for player in self._players if player.user_id == user_id), None)
        if to_remove is None:
            raise GameTableInternalException(
                reason="player_not_found", detail="Could not remove player: player not found"
            )
        self._players.remove(to_remove)

    def remove_bot_player(self, seat_number: SeatNumber, initiated_by: int) -> None:
        self._validate_status(acceptable_statuses={TableStatus.NOT_STARTED})
        self._validate_is_owner(initiated_by)
        to_remove = next((player for player in self._players if player.seat_number == seat_number), None)
        if to_remove is None:
            raise GameTableRulesException(
                reason="bot_player_not_found", detail="Could not remove bot player: bot player not found"
            )
        self._players.remove(to_remove)

    def start_game(self, initiated_by: int) -> Sequence[GameEvent]:
        # TODO: maybe check if all players have agreed to start according to table config
        self._validate_status(acceptable_statuses={TableStatus.NOT_STARTED})
        self._validate_is_owner(initiated_by)
        self._validate_has_enough_players()
        game_state, events = self._engine.start_game(self._config.game_config, self.taken_seat_numbers)
        self._game_state = game_state
        self._status = TableStatus.IN_PROGRESS
        return events

    # regular turn is a turn taken by a human player by providing a command
    def take_regular_turn(self, user_id: int, command: GameCommand) -> Sequence[GameEvent]:
        self._validate_status(acceptable_statuses={TableStatus.IN_PROGRESS})
        if self.active_player.user_id != user_id:
            raise GameTableRulesException(reason="not_player_turn", detail="Could not take turn: not the player's turn")
        return self._take_turn(self.game_state, command)

    # automatic turn is a turn taken by a bot player by producing a command
    # it may take some time to create a command using bot strategy if some complicated algorithm or external service is used
    def take_automatic_turn(self, initiated_by: int) -> Sequence[GameEvent]:
        self._validate_status(acceptable_statuses={TableStatus.IN_PROGRESS})
        self._validate_is_player(initiated_by)
        active_player = self.active_player
        if not active_player.is_bot:
            raise GameTableRulesException(reason="not_bot_turn", detail="Could not take turn: not a bot's turn")
        bot_strategy = active_player.bot_strategy
        if bot_strategy is None:
            raise GameTableInternalException(
                reason="bot_strategy_not_set",
                detail=f"Could not take bot's turn: bot strategy is not set for bot {active_player.screen_name}",
            )
        game_state = self.game_state
        command = bot_strategy.create_command(game_state)
        return self._take_turn(game_state, command)

    def _take_turn(self, game_state: GameState, command: GameCommand) -> Sequence[GameEvent]:
        game_state_updated, events = self._engine.process_command(game_state, command)
        if game_state_updated.is_finished:
            self._status = TableStatus.FINISHED
        self._game_state = game_state_updated
        return events

    # can cancel only not-finished/aborted games
    def cancel_game(self, initiated_by: int) -> None:
        self._validate_status(unacceptable_statuses={TableStatus.FINISHED, TableStatus.ABORTED})
        self._validate_is_owner(initiated_by)
        self._status = TableStatus.CANCELLED

    # this should mark game as aborted (because player left or was kicked by owner for some reason) and link the user_id who to blame for this
    # so that user's reputation can be affected etc... just a reminder for later when these features come in
    # def abort_game(self, caused_by_user_id: int) -> None: ...

    def restore_game_state(self, events: Sequence[GameEvent]) -> None:
        restored_game_state = self._engine.restore_game_state(events, self._config.game_config, self.taken_seat_numbers)
        self._game_state = restored_game_state
        return None

    ###  Helper methods ###

    def _generate_seat_number(self, choices: set[SeatNumber]) -> SeatNumber:
        return random.choice(list(choices))

    def _generate_bot_player_id(self) -> str:
        return "bot-" + str(uuid.uuid4())

    def _get_seat_number(self, preferred_seat_number: SeatNumber | None = None) -> SeatNumber:
        taken_seat_numbers = {player.seat_number for player in self.players}
        available_seat_numbers = set(self._config.possible_seat_numbers) - taken_seat_numbers
        # if seat number is not provided, choose random one. if it is provided, use it if it is available
        if preferred_seat_number is not None:
            if preferred_seat_number not in available_seat_numbers:
                raise GameTableRulesException(
                    reason="seat_number_not_available",
                    detail=f"Could not add player: preferred seat number {preferred_seat_number} is not available at the table",
                )
            available_seat_numbers = {preferred_seat_number}
        return self._generate_seat_number(available_seat_numbers)

    ###  Validation methods ###

    def _validate_bots_allowed(self) -> None:
        if not self._config.table_config.bots_allowed:
            raise GameTableRulesException(
                reason="bots_not_allowed", detail="Could not add bot player: bots are not allowed at the table"
            )

    def _validate_can_join_table(self, user_id: int) -> None:
        if user_id in [player.user_id for player in self._players]:
            raise GameTableRulesException(
                reason="player_already_exists", detail="Could not add player: user already exists at the table"
            )

    def _validate_is_owner(self, user_id: int) -> None:
        if self.owner_id != user_id:
            raise GameTableRulesException(
                reason="not_table_owner", detail="Could not perform action: not the table owner"
            )

    def _validate_is_player(self, user_id: int) -> None:
        if user_id not in [player.user_id for player in self._players]:
            raise GameTableRulesException(
                reason="not_player_of_table", detail="Could not perform action: not a player of the table"
            )

    def _validate_status(
        self, acceptable_statuses: set[TableStatus] | None = None, unacceptable_statuses: set[TableStatus] | None = None
    ) -> None:
        if acceptable_statuses is not None and self.status not in acceptable_statuses:
            raise GameTableRulesException(
                reason="invalid_table_status",
                detail="Could not perform action: table is not in the one of the correct statuses",
            )
        if unacceptable_statuses is not None and self.status in unacceptable_statuses:
            raise GameTableRulesException(
                reason="invalid_table_status",
                detail="Could not perform action: table is in the one of the unacceptable statuses",
            )

    def _validate_has_free_seats(self) -> None:
        if len(self._players) >= self._config.table_config.max_seats:
            raise GameTableRulesException(reason="table_full", detail="Could not add player: table is full")

    def _validate_has_enough_players(self) -> None:
        if len(self._players) < self._config.table_config.min_seats:
            raise GameTableRulesException(
                reason="not_enough_players", detail="Could not start game: not enough players to start the game"
            )

    def to_dict(self) -> dict[str, Any]:
        """Serialize to JSON-compatible dict"""
        return {
            "id": self._id,
            "config": self._config.to_dict(),
            "players": [player.to_dict() for player in self._players],
            "owner_id": self._owner_id,
            "game_state": self._game_state.to_dict() if self._game_state else None,
            "status": self._status.value,
        }

    def to_public_dict(self, seat_number: SeatNumber | None = None) -> dict[str, Any]:
        return {
            "id": self._id,
            "config": self._config.to_dict(),
            "players": [player.to_dict() for player in self._players],
            "owner_id": self._owner_id,
            "game_state": self._game_state.to_public_dict(seat_number) if self._game_state else None,
            "status": self._status.value,
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

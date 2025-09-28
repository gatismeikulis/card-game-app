from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from ..common.command import Command
from ..common.event import Event
from ..common.game_state import GameState

TGameState = TypeVar("TGameState", bound=GameState)
TCommand = TypeVar("TCommand", bound=Command)
TEvent = TypeVar("TEvent", bound=Event)


class GameEngine(ABC, Generic[TGameState, TCommand, TEvent]):
    @abstractmethod
    def init_game(self) -> TGameState: ...

    @abstractmethod
    def process_command(self, game_state: TGameState, command: TCommand) -> tuple[TGameState, list[TEvent]]: ...

    @abstractmethod
    def create_automatic_command(self, game_state: TGameState) -> TCommand: ...

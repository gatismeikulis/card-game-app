from abc import ABC, abstractmethod
from typing import Generic, TypeVar

TGameState = TypeVar("TGameState")
TCommand = TypeVar("TCommand")
TEvent = TypeVar("TEvent")


class GameEngine(ABC, Generic[TGameState, TCommand, TEvent]):
    @abstractmethod
    def init_game(self) -> TGameState: ...

    @abstractmethod
    def process_command(self, game_state: TGameState, command: TCommand) -> tuple[TGameState, list[TEvent]]: ...

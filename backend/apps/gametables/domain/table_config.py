from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Self


@dataclass(frozen=True)
class TableConfig(ABC):
    """Table-level configuration for game table

    This configuration does not effect directly affect the output of the game engine.
    Max and min player count is a table-level configuration. But it must be according to specific game rules. for example, five_hundred game allows stricly 3 players.
    But poker table can allow from 2 to 10 players possibly.
    Another example, automatic start of the game is a table-level configuration - if it's true, the game will start automatically when necessary player count is reached without asking players to agree to start.
    Another example is bots_allowed - if it's true, the game will allow bots to join the table.
    Another example is if game is real time or turn based.
    """

    automatic_start: bool  # true - start game automatically without asking players to agree to start
    bots_allowed: bool  # true - allow bots to join the table
    min_seats: int  # minimum number of players for game to happen
    max_seats: int  # maximum number of players for game to happen

    @abstractmethod
    def to_dict(self) -> dict[str, Any]: ...

    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict[str, Any]) -> Self: ...

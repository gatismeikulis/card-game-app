from collections.abc import Set
from dataclasses import dataclass
from typing import Any

from .table_config import TableConfig
from game.common.game_config import GameConfig
from game.common.seat import SeatNumber
from game.game_name import GameName


@dataclass(frozen=True, slots=True)
class GameTableConfig:
    game_name: GameName
    game_config: GameConfig
    table_config: TableConfig

    @property
    def possible_seat_numbers(self) -> Set[SeatNumber]:
        return frozenset(range(1, self.game_config.max_seats + 1))

    def to_dict(self) -> dict[str, Any]:
        """Serialize to JSON-compatible dict"""
        return {
            "game_name": self.game_name.value,
            "game_config": self.game_config.to_dict(),
            "table_config": self.table_config.to_dict(),
        }

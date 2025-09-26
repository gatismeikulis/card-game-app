from dataclasses import dataclass

from backend.domain.game.common.seat import SeatNumber
from backend.domain.game.game_name import GameName


@dataclass(frozen=True, slots=True)
class GameTableConfig:
    game_name: GameName
    min_players: int
    max_players: int
    automatic_start: bool

    @property
    def possible_seat_numbers(self) -> set[SeatNumber]:
        return set(range(1, self.max_players + 1))

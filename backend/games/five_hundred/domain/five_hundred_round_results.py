from collections.abc import Mapping
from dataclasses import dataclass

from .five_hundred_seat import FiveHundredSeat


@dataclass(frozen=True, slots=True)
class FiveHundredRoundResults:
    _round_number: int
    _bidding_results: tuple[FiveHundredSeat, int] | None
    _seat_points: Mapping[FiveHundredSeat, int]

    @property
    def round_number(self) -> int:
        return self._round_number

    @property
    def bidding_results(self) -> tuple[FiveHundredSeat, int] | None:
        return self._bidding_results

    @property
    def seat_points(self) -> Mapping[FiveHundredSeat, int]:
        return self._seat_points

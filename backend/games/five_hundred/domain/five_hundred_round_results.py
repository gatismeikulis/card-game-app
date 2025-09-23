from collections.abc import Mapping
from dataclasses import dataclass

from .five_hundred_seat import FiveHundredSeat


@dataclass(frozen=True, slots=True)
class FiveHundredRoundResults:
    round_number: int
    bidding_results: tuple[FiveHundredSeat, int] | None
    seat_points: Mapping[FiveHundredSeat, int]

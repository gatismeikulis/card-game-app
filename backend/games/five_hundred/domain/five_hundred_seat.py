from dataclasses import dataclass
from typing import override
from backend.games.common.seat import Seat


@dataclass(frozen=True, slots=True, repr=False)
class FiveHundredSeat(Seat):

    @override
    def next(self) -> "FiveHundredSeat":
        if self.number == 3:
            return FiveHundredSeat(1)
        else:
            return FiveHundredSeat(self.number + 1)

    @override
    def prev(self) -> "FiveHundredSeat":
        if self.number == 1:
            return FiveHundredSeat(3)
        else:
            return FiveHundredSeat(self.number - 1)

    @classmethod
    @override
    def from_int(cls, number: int) -> "FiveHundredSeat":
        return FiveHundredSeat(number)  # TODO: consider adding some kind of validation here

from dataclasses import dataclass
from typing import Self, override

from .constants import MAX_SEATS
from ...common.seat import Seat


@dataclass(frozen=True, slots=True, repr=False)
class FiveHundredSeat(Seat):
    @override
    def next(self) -> Self:
        if self.number >= MAX_SEATS:
            return type(self)(number=1)
        else:
            return type(self)(self.number + 1)

    @override
    def prev(self) -> Self:
        if self.number <= 1:
            return type(self)(MAX_SEATS)
        else:
            return type(self)(self.number - 1)

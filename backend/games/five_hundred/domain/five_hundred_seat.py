from enum import Enum
from typing import override


# Seat is the position of the player at the table. Since game only has 3 players, there are only 3 seats
class FiveHundredSeat(Enum):
    ONE = 1
    TWO = 2
    THREE = 3

    @property
    def next(self) -> "FiveHundredSeat":
        if self is FiveHundredSeat.ONE:
            return FiveHundredSeat.TWO
        elif self is FiveHundredSeat.TWO:
            return FiveHundredSeat.THREE
        else:
            return FiveHundredSeat.ONE

    @property
    def prev(self) -> "FiveHundredSeat":
        if self is FiveHundredSeat.ONE:
            return FiveHundredSeat.THREE
        elif self is FiveHundredSeat.TWO:
            return FiveHundredSeat.ONE
        else:
            return FiveHundredSeat.TWO

    @override
    def __str__(self) -> str:
        return f"<{self.value}>"

    @override
    def __repr__(self) -> str:
        return self.__str__()

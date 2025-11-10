from collections.abc import Collection
from dataclasses import dataclass
from typing import override

from .game_exception import GameEngineException

type SeatNumber = int


@dataclass(frozen=True, slots=True)
class Seat:
    number: SeatNumber

    def next(self, possible_seats: Collection["Seat"]) -> "Seat":
        if len(possible_seats) == 0:
            raise GameEngineException(detail="Could not get next seat: no possible seats given")
        if self.number >= max(seat.number for seat in possible_seats):
            return Seat(min(seat.number for seat in possible_seats))
        else:
            next_num = min(seat.number for seat in possible_seats if seat.number > self.number)
            return Seat(next_num)

    def prev(self, possible_seats: Collection["Seat"]) -> "Seat":
        if len(possible_seats) == 0:
            raise GameEngineException(detail="Could not get previous seat: no possible seats given")
        if self.number <= min(seat.number for seat in possible_seats):
            return Seat(max(seat.number for seat in possible_seats))
        else:
            prev_num = max(seat.number for seat in possible_seats if seat.number < self.number)
            return Seat(prev_num)

    def to_dict(self) -> str:
        """Serialize to seat number"""
        return str(self.number)

    @staticmethod
    def from_dict(data: int) -> "Seat":
        """Reconstruct from seat number"""
        return Seat(int(data))

    @override
    def __str__(self) -> str:
        return f"-{self.number}-"

    @override
    def __repr__(self) -> str:
        return self.__str__()

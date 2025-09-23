from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import override

from .five_hundred_seat import FiveHundredSeat
from .five_hundred_round import FiveHundredRound
from .five_hundred_round_results import FiveHundredRoundResults
from .constants import GAME_STARTING_POINTS


@dataclass(frozen=True, slots=True)
class FiveHundredGame:
    round: FiveHundredRound  # current round
    results: Sequence[FiveHundredRoundResults]  # round-by-round results
    summary: Mapping[FiveHundredSeat, int]  # running game-points

    @staticmethod
    def create(round: FiveHundredRound) -> "FiveHundredGame":
        return FiveHundredGame(
            round=round,
            results=[],
            summary={
                FiveHundredSeat(1): GAME_STARTING_POINTS,
                FiveHundredSeat(2): GAME_STARTING_POINTS,
                FiveHundredSeat(3): GAME_STARTING_POINTS,
            },
        )

    @property
    def winner(self) -> FiveHundredSeat | None:
        return next((seat for seat, points in self.summary.items() if points <= 0), None)

    @override
    def __str__(self) -> str:
        return f"""
SUMMARY: {self.summary}
ROUND {self.round.round_number} - {self.round.phase} | ACTIVE SEAT: {self.round.active_seat} 
REQUIRED SUIT: {self.round.required_suit} | TRUMP: {self.round.trump_suit} | HIGHEST BID: {self.round.highest_bid if self.round.highest_bid else "None"}

SEAT 1: {self.round.seat_infos[FiveHundredSeat(1)]}
SEAT 2: {self.round.seat_infos[FiveHundredSeat(2)]}
SEAT 3: {self.round.seat_infos[FiveHundredSeat(3)]}

CARDS TO TAKE: {self.round.cards_to_take}
CARDS ON BOARD: {self.round.cards_on_board}
"""

    @override
    def __repr__(self) -> str:
        return self.__str__()

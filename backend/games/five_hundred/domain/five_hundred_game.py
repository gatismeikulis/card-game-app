from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import override

from backend.games.common.game_state import GameState

from .five_hundred_seat import FiveHundredSeat
from .five_hundred_round import FiveHundredRound
from .five_hundred_round_results import FiveHundredRoundResults
from .constants import GAME_STARTING_POINTS


@dataclass(frozen=True, slots=True)
class FiveHundredGame(GameState):
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
    @override
    def active_seat(self) -> FiveHundredSeat:
        return self.round.active_seat

    @property
    def winner(self) -> FiveHundredSeat | None:
        return next((seat for seat, points in self.summary.items() if points <= 0), None)

    @override
    def __str__(self) -> str:
        return f"""
SUMMARY: {self.summary}
ROUND {self.round.round_number}, {self.round.phase} | Seat {self.round.active_seat} is playing
Required {self.round.required_suit if self.round.required_suit else "-"} | Trump is {self.round.trump_suit if self.round.trump_suit else "-"} | {f"Highest bid is {self.round.highest_bid[1]} by {self.round.highest_bid[0]}" if self.round.highest_bid else "-"}

{FiveHundredSeat(1)} {self.round.seat_infos[FiveHundredSeat(1)]}
{FiveHundredSeat(2)} {self.round.seat_infos[FiveHundredSeat(2)]}
{FiveHundredSeat(3)} {self.round.seat_infos[FiveHundredSeat(3)]}

CARDS TO TAKE: {self.round.cards_to_take}
CARDS ON BOARD: {' ==> '.join(f'{k} {v}' for k, v in self.round.cards_on_board.items() if v)}
"""

    @override
    def __repr__(self) -> str:
        return self.__str__()

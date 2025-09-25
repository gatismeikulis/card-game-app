from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import override

from ...common.game_state import GameState
from .constants import GAME_STARTING_POINTS
from .five_hundred_phase import FiveHundredPhase
from .five_hundred_round import FiveHundredRound
from .five_hundred_round_results import FiveHundredRoundResults
from .five_hundred_seat import FiveHundredSeat
from .five_hundred_seat_info import FiveHundredSeatInfo


@dataclass(frozen=True, slots=True)
class FiveHundredGame(GameState):
    round: FiveHundredRound  # current round
    results: Sequence[FiveHundredRoundResults]  # round-by-round results
    summary: Mapping[FiveHundredSeat, int]  # running game-points
    active_seat: FiveHundredSeat

    @staticmethod
    def create(round: FiveHundredRound) -> "FiveHundredGame":
        return FiveHundredGame(
            active_seat=round.first_seat,
            round=round,
            results=[],
            summary={
                FiveHundredSeat(1): GAME_STARTING_POINTS,
                FiveHundredSeat(2): GAME_STARTING_POINTS,
                FiveHundredSeat(3): GAME_STARTING_POINTS,
            },
        )

    @property
    def winners(self) -> Sequence[FiveHundredSeat] | None:
        if self.round.phase != FiveHundredPhase.GAME_FINISHED:
            return None
        return [seat for seat, points in self.summary.items() if points <= 0]

    @property
    def active_seats_info(self) -> FiveHundredSeatInfo:
        return self.round.seat_infos[self.active_seat]

    @override
    def __str__(self) -> str:
        if self.round.phase == FiveHundredPhase.GAME_FINISHED:
            return f"""
SUMMARY: {self.summary}
WINNERS: {self.winners}
"""
        return f"""
SUMMARY: {self.summary}
ROUND {self.round.round_number}, {self.round.phase} | Seat {self.active_seat} is playing
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

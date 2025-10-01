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
    def winners(self) -> Sequence[FiveHundredSeat]:
        if self.round.phase != FiveHundredPhase.GAME_FINISHED:
            raise ValueError("Game is not finished")
        return [seat for seat, points in self.summary.items() if points <= 0]

    @property
    def active_seats_info(self) -> FiveHundredSeatInfo:
        return self.round.seat_infos[self.active_seat]

    @override
    def str_repr_for_table(self) -> str:
        match self.round.phase:
            case FiveHundredPhase.GAME_FINISHED:
                return f"Game Finished, Winners: {", ".join(str(seat) for seat in self.winners)}, Final Scores: {", ".join(f"{seat}: {self.summary[seat]}" for seat in self.summary.keys())}"
            case _:
                return f"Game in progress, Round {self.round.round_number}, {self.round.phase}, Seat {self.active_seat} is taking turn, Current scores: {", ".join(f"{seat}: {self.summary[seat]}" for seat in self.summary.keys())}"

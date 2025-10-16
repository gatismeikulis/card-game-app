from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any, override

from ...common.seat import SeatNumber
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
    is_finished: bool

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
            is_finished=False,
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
                return f"Game Finished, Winners: {', '.join(str(seat) for seat in self.winners)}, Final Scores: {', '.join(f'{seat}: {self.summary[seat]}' for seat in self.summary.keys())}"
            case _:
                return f"Game in progress, Round {self.round.round_number}, {self.round.phase}, Seat {self.active_seat} is taking turn, Current scores: {', '.join(f'{seat}: {self.summary[seat]}' for seat in self.summary.keys())}"

    def to_dict(self) -> dict[str, Any]:
        """Serialize to JSON-compatible dict"""
        return {
            "round": self.round.to_dict(),
            "results": [result.to_dict() for result in self.results],
            "summary": {seat.to_dict(): points for seat, points in self.summary.items()},
            "active_seat": self.active_seat.to_dict(),
            "is_finished": self.is_finished,
        }

    @staticmethod
    def from_dict(data: dict[str, Any]) -> "FiveHundredGame":
        """Reconstruct from JSON-compatible dict"""
        return FiveHundredGame(
            round=FiveHundredRound.from_dict(data["round"]),
            results=[FiveHundredRoundResults.from_dict(result) for result in data["results"]],
            summary={FiveHundredSeat.from_dict(int(seat)): points for seat, points in data["summary"].items()},
            active_seat=FiveHundredSeat.from_dict(data["active_seat"]),
            is_finished=data["is_finished"],
        )

    def to_public_dict(self, seat_number: SeatNumber | None = None) -> dict[str, Any]:
        """Serialize to JSON-compatible dict, but exclude non-public information except specifics for given seat"""
        return {
            "round": {
                "phase": self.round.phase.value,
                "round_number": self.round.round_number,
                "first_seat": self.round.first_seat.to_dict(),
                "is_marriage_announced": self.round.is_marriage_announced,
                "required_suit": self.round.required_suit.symbol if self.round.required_suit else None,
                "trump_suit": self.round.trump_suit.symbol if self.round.trump_suit else None,
                "highest_bid": [self.round.highest_bid[0].to_dict(), self.round.highest_bid[1]]
                if self.round.highest_bid
                else None,
                "cards_on_board": {
                    seat.to_dict(): card.to_dict() if card else None for seat, card in self.round.cards_on_board.items()
                },
                "seat_infos": {
                    seat.to_dict(): (
                        info.to_dict()
                        if seat.number == seat_number  # Full info for specific seat
                        else info.to_public_dict()  # Public info by default
                    )
                    for seat, info in self.round.seat_infos.items()
                },
            },
            "results": [result.to_dict() for result in self.results],
            "summary": {seat.to_dict(): points for seat, points in self.summary.items()},
            "active_seat": self.active_seat.to_dict(),
        }

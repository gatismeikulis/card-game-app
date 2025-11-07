from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any, Self, override

from ...common.game_ending import GameEnding
from ...common.game_config import GameConfig
from ...common.seat import Seat
from ...common.game_exception import GameEngineException
from ...common.seat import SeatNumber
from ...common.game_state import GameState
from .constants import GAME_STARTING_POINTS
from .five_hundred_game_config import FiveHundredGameConfig
from .five_hundred_phase import FiveHundredPhase
from .five_hundred_round import FiveHundredRound
from .five_hundred_round_results import FiveHundredRoundResults
from .five_hundred_seat_info import FiveHundredSeatInfo


@dataclass(frozen=True, slots=True)
class FiveHundredGame(GameState):
    round: FiveHundredRound  # current round
    results: Sequence[
        FiveHundredRoundResults
    ]  # round-by-round results TODO: consider moving this out of the game state...
    summary: Mapping[Seat, int]  # running game-points
    active_seat: Seat
    ending: GameEnding | None
    game_config: FiveHundredGameConfig
    taken_seats: frozenset[Seat]
    turn_number: int

    @override
    @classmethod
    def init(cls, game_config: GameConfig, taken_seat_numbers: frozenset[SeatNumber]) -> Self:
        if not isinstance(game_config, FiveHundredGameConfig):
            raise GameEngineException(
                detail=f"Could not start the game: expected FiveHundredGameConfig, got {type(game_config).__name__}"
            )
        taken_seats: frozenset[Seat] = frozenset(Seat(number) for number in taken_seat_numbers)

        round = FiveHundredRound.create(1, Seat(min(taken_seat_numbers)), taken_seats)
        return cls(
            active_seat=round.first_seat,
            round=round,
            results=[],
            summary={seat: GAME_STARTING_POINTS for seat in taken_seats},
            ending=None,
            game_config=game_config,
            taken_seats=taken_seats,
            turn_number=0,
        )

    @property
    def active_seats_info(self) -> FiveHundredSeatInfo:
        return self.round.seat_infos[self.active_seat]

    @override
    def str_repr_for_table(self) -> str:
        match self.round.phase:
            case FiveHundredPhase.GAME_ENEDED:
                return f"Game Ended, Final Scores: {', '.join(f'{seat}: {self.summary[seat]}' for seat in self.summary.keys())}"
            case _:
                return f"Game in progress, Round {self.round.round_number}, {self.round.phase}, Seat {self.active_seat} is taking turn, Current scores: {', '.join(f'{seat}: {self.summary[seat]}' for seat in self.summary.keys())}"

    @override
    def to_dict(self) -> dict[str, Any]:
        """Serialize to JSON-compatible dict"""
        return {
            "round": self.round.to_dict(),
            "results": [result.to_dict() for result in self.results],
            "summary": {seat.to_dict(): points for seat, points in self.summary.items()},
            "active_seat": self.active_seat.to_dict(),
            "ending": self.ending.to_dict() if self.ending else None,
            "game_config": self.game_config.to_dict(),
            "taken_seats": [seat.to_dict() for seat in self.taken_seats],
            "turn_number": self.turn_number,
        }

    @override
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        """Reconstruct from JSON-compatible dict"""
        return cls(
            round=FiveHundredRound.from_dict(data["round"]),
            results=[FiveHundredRoundResults.from_dict(result) for result in data["results"]],
            summary={Seat.from_dict(int(seat)): points for seat, points in data["summary"].items()},
            active_seat=Seat.from_dict(data["active_seat"]),
            ending=GameEnding.from_dict(data["ending"]) if data["ending"] else None,
            game_config=FiveHundredGameConfig.from_dict(data["game_config"]),
            taken_seats=frozenset(Seat.from_dict(int(seat)) for seat in data["taken_seats"]),
            turn_number=data["turn_number"],
        )

    @override
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
                "prev_trick": [card.to_dict() for card in self.round.prev_trick],
                "ending": self.ending.to_dict() if self.ending else None,
                "seat_infos": {
                    seat.to_dict(): (
                        info.to_dict()
                        if seat.number == seat_number  # Full info for specific seat
                        else info.to_public_dict()  # Public info by default
                    )
                    for seat, info in self.round.seat_infos.items()
                },
            },
            "summary": {seat.to_dict(): points for seat, points in self.summary.items()},
            "active_seat": self.active_seat.to_dict(),
            "is_my_turn": self.active_seat.number == seat_number,
            "turn_number": self.turn_number,
        }

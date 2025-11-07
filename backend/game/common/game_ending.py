from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from enum import Enum
from typing import Any

from .game_exception import GameParsingException
from .seat import Seat


class GameEndingReason(Enum):
    FINISHED = "finished"  # finished because game reached its natural end...
    ABORTED = "aborted"  # aborted because some player left or was kicked out...
    CANCELLED = "cancelled"  # cancelled because players agreed to cancel the game...or admin cancelled the game...

    @staticmethod
    def from_string(reason: str) -> "GameEndingReason":
        match reason.upper():
            case "FINISHED":
                return GameEndingReason.FINISHED
            case "ABORTED":
                return GameEndingReason.ABORTED
            case "CANCELLED":
                return GameEndingReason.CANCELLED
            case _:
                raise GameParsingException(
                    reason="game_ending_reason_parsing_error",
                    detail=f"Could not parse game ending reason from input: {reason}",
                )


@dataclass(frozen=True, slots=True)
class GameEnding:
    winners: Sequence[Seat]
    losers: Sequence[Seat]
    reason: GameEndingReason
    point_differences: Mapping[
        Seat, int
    ]  # generic points - difference between starting points and ending points. the meaning of this is game-specific.

    def to_dict(self) -> dict[str, Any]:
        """Serialize to seat number"""
        return {
            "winners": [seat.to_dict() for seat in self.winners],
            "losers": [seat.to_dict() for seat in self.losers],
            "reason": self.reason.value,
            "point_differences": {seat.to_dict(): points for seat, points in self.point_differences.items()},
        }

    @staticmethod
    def from_dict(data: dict[str, Any]) -> "GameEnding":
        return GameEnding(
            winners=[Seat.from_dict(seat) for seat in data["winners"]],
            losers=[Seat.from_dict(seat) for seat in data["losers"]],
            reason=GameEndingReason(data["reason"]),
            point_differences={Seat.from_dict(seat): points for seat, points in data["point_differences"].items()},
        )

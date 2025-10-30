from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

from ...common.seat import Seat


@dataclass(frozen=True, slots=True)
class FiveHundredRoundResults:
    round_number: int
    bidding_results: tuple[Seat, int] | None
    seat_points: Mapping[Seat, int]

    def to_dict(self) -> dict[str, Any]:
        """Serialize to JSON-compatible dict"""
        return {
            "round_number": self.round_number,
            "bidding_results": [
                self.bidding_results[0].to_dict(),
                self.bidding_results[1],
            ]
            if self.bidding_results
            else None,
            "seat_points": {seat.to_dict(): points for seat, points in self.seat_points.items()},
        }

    @staticmethod
    def from_dict(data: dict[str, Any]) -> "FiveHundredRoundResults":
        """Reconstruct from JSON-compatible dict"""
        # Reconstruct bidding_results tuple
        bidding_results = None
        if data["bidding_results"]:
            bidding_results = (
                Seat.from_dict(data["bidding_results"][0]),
                data["bidding_results"][1],
            )

        return FiveHundredRoundResults(
            round_number=data["round_number"],
            bidding_results=bidding_results,
            seat_points={Seat.from_dict(int(seat_num)): points for seat_num, points in data["seat_points"].items()},
        )

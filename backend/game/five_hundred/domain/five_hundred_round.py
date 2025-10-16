from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any

from ...common.card import Suit
from ...common.deck import Deck
from ...common.hand import Hand
from .constants import CARDS_IN_STARTING_HAND, CARDS_TO_TAKE
from .five_hundred_card import FiveHundredCard
from .five_hundred_phase import FiveHundredPhase
from .five_hundred_seat import FiveHundredSeat
from .five_hundred_seat_info import FiveHundredSeatInfo


@dataclass(frozen=True, slots=True)
class FiveHundredRound:
    seat_infos: Mapping[FiveHundredSeat, FiveHundredSeatInfo]
    cards_on_board: Mapping[FiveHundredSeat, FiveHundredCard | None]
    cards_to_take: Sequence[FiveHundredCard]
    required_suit: Suit | None
    trump_suit: Suit | None
    highest_bid: tuple[FiveHundredSeat, int] | None
    phase: FiveHundredPhase
    round_number: int
    first_seat: FiveHundredSeat  # seat which started this round
    is_marriage_announced: bool

    @staticmethod
    def create(deck: Deck[FiveHundredCard], round_number: int, first_seat: FiveHundredSeat) -> "FiveHundredRound":
        cards_to_take = deck.draw_many(CARDS_TO_TAKE)
        seat_one_cards = deck.draw_many(CARDS_IN_STARTING_HAND)
        seat_two_cards = deck.draw_many(CARDS_IN_STARTING_HAND)
        seat_three_cards = deck.draw_many(CARDS_IN_STARTING_HAND)

        seat_infos: Mapping[FiveHundredSeat, FiveHundredSeatInfo] = {
            FiveHundredSeat(1): FiveHundredSeatInfo(
                hand=Hand(tuple(seat_one_cards)),
                bid=0,
                points=0,
                trick_count=0,
                marriage_points=[],
            ),
            FiveHundredSeat(2): FiveHundredSeatInfo(
                hand=Hand(tuple(seat_two_cards)),
                bid=0,
                points=0,
                trick_count=0,
                marriage_points=[],
            ),
            FiveHundredSeat(3): FiveHundredSeatInfo(
                hand=Hand(tuple(seat_three_cards)),
                bid=0,
                points=0,
                trick_count=0,
                marriage_points=[],
            ),
        }

        cards_on_board: Mapping[FiveHundredSeat, FiveHundredCard | None] = {
            FiveHundredSeat(1): None,
            FiveHundredSeat(2): None,
            FiveHundredSeat(3): None,
        }

        return FiveHundredRound(
            seat_infos=seat_infos,
            cards_on_board=cards_on_board,
            cards_to_take=cards_to_take,
            required_suit=None,
            trump_suit=None,
            highest_bid=None,
            phase=FiveHundredPhase.BIDDING,
            round_number=round_number,
            first_seat=first_seat,
            is_marriage_announced=False,
        )

    @property
    def cards_on_board_count(self) -> int:
        return sum(1 for v in self.cards_on_board.values() if v is not None)

    def to_dict(self) -> dict[str, Any]:
        """Serialize to JSON-compatible dict"""
        return {
            "seat_infos": {seat.to_dict(): info.to_dict() for seat, info in self.seat_infos.items()},
            "cards_on_board": {
                seat.to_dict(): card.to_dict() if card else None for seat, card in self.cards_on_board.items()
            },
            "cards_to_take": [card.to_dict() for card in self.cards_to_take],
            "required_suit": self.required_suit.symbol if self.required_suit else None,
            "trump_suit": self.trump_suit.symbol if self.trump_suit else None,
            "highest_bid": [self.highest_bid[0].to_dict(), self.highest_bid[1]] if self.highest_bid else None,
            "phase": self.phase.value,
            "round_number": self.round_number,
            "first_seat": self.first_seat.to_dict(),
            "is_marriage_announced": self.is_marriage_announced,
        }

    @staticmethod
    def from_dict(data: dict[str, Any]) -> "FiveHundredRound":
        """Reconstruct from JSON-compatible dict"""
        return FiveHundredRound(
            seat_infos={
                FiveHundredSeat.from_dict(int(seat_num)): FiveHundredSeatInfo.from_dict(info)
                for seat_num, info in data["seat_infos"].items()
            },
            cards_on_board={
                FiveHundredSeat.from_dict(int(seat_num)): FiveHundredCard.from_dict(card) if card else None
                for seat_num, card in data["cards_on_board"].items()
            },
            cards_to_take=[FiveHundredCard.from_dict(card) for card in data["cards_to_take"]],
            required_suit=Suit.from_string(data["required_suit"]) if data["required_suit"] else None,
            trump_suit=Suit.from_string(data["trump_suit"]) if data["trump_suit"] else None,
            highest_bid=(
                FiveHundredSeat.from_dict(data["highest_bid"][0]),
                data["highest_bid"][1],
            )
            if data["highest_bid"]
            else None,
            phase=FiveHundredPhase(data["phase"]),
            round_number=data["round_number"],
            first_seat=FiveHundredSeat.from_dict(data["first_seat"]),
            is_marriage_announced=data["is_marriage_announced"],
        )

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any, override

from ...common.card import Suit
from ...common.hand import Hand
from .five_hundred_card import FiveHundredCard


# Seat info is round-specific information about a player
@dataclass(frozen=True, slots=True)
class FiveHundredSeatInfo:
    hand: Hand[FiveHundredCard]
    bid: int  # negative value means the player has passed, 0 means the player has not bid yet
    points: int  # card-points this round so far, resets to 0 at the beginning of each round
    trick_count: int  # not essential for the game, but useful for better UI
    marriage_points: Sequence[int]  # not essential for the game, but useful for better UI

    def cards_allowed_to_play(self, required_suit: Suit | None, trump_suit: Suit | None) -> Sequence[FiveHundredCard]:
        if required_suit is None:
            return self.hand.cards
        if trump_suit is None:
            return self.hand.cards
        cards_matching_required_suit = [card for card in self.hand.cards if card.suit == required_suit]
        if len(cards_matching_required_suit) == 0:
            cards_matching_trump = [card for card in self.hand.cards if card.suit == trump_suit]
            if len(cards_matching_trump) == 0:
                return self.hand.cards
            else:
                return cards_matching_trump
        else:
            return cards_matching_required_suit

    def to_dict(self) -> dict[str, Any]:
        """Serialize to JSON-compatible dict"""
        return {
            "hand": self.hand.to_dict(),
            "bid": self.bid,
            "points": self.points,
            "trick_count": self.trick_count,
            "marriage_points": list(self.marriage_points),
        }

    @staticmethod
    def from_dict(data: dict[str, Any]) -> "FiveHundredSeatInfo":
        """Reconstruct from JSON-compatible dict"""
        return FiveHundredSeatInfo(
            hand=Hand.from_dict(data["hand"], FiveHundredCard),
            bid=data["bid"],
            points=data["points"],
            trick_count=data["trick_count"],
            marriage_points=data["marriage_points"],
        )

    def to_public_dict(self) -> dict[str, Any]:
        """Serialize to JSON-compatible dict, but exclude non-public information"""
        return {
            "hand": len(self.hand.cards),
            "bid": self.bid,
            "points": None,
            "trick_count": self.trick_count,
            "marriage_points": None,
        }

    @override
    def __str__(self) -> str:
        return f"{self.hand} | {self.bid if self.bid >= 0 else 'passed'} | {self.points} points from {self.trick_count} tricks {self.marriage_points if self.marriage_points else ''}"

    @override
    def __repr__(self) -> str:
        return self.__str__()

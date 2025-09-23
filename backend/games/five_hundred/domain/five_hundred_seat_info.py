from collections.abc import Sequence
from dataclasses import dataclass
from typing import override

from ...common.card import Suit
from .five_hundred_card import FiveHundredCard
from ...common.hand import Hand


# Seat info is the round-specific information about a player
@dataclass(frozen=True, slots=True)
class FiveHundredSeatInfo:
    hand: Hand[FiveHundredCard]
    bid: int  # negative value means the player has passed, 0 means the player has not bid yet
    points: int  # card-points this round so far, resets to 0 at the beginning of each round
    trick_count: int  # not essential for the game, but useful for better UI
    marriage_points: Sequence[int]  # not essential for the game, but useful for better UI

    @override
    def __str__(self) -> str:
        return f"{self.hand} | BID:{self.bid} | POINTS: {self.points} | TRICK COUNT:{self.trick_count} | {self.marriage_points}"

    @override
    def __repr__(self) -> str:
        return self.__str__()

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

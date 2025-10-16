from dataclasses import dataclass
from typing import override

from ...common.card import Rank, Suit
from ...common.deck import Deck
from .five_hundred_card import FiveHundredCard

# Game 'Five Hundred' only uses 24 card deck, from 9 to Ace of each suit
RANKS = [Rank.NINE, Rank.JACK, Rank.QUEEN, Rank.KING, Rank.TEN, Rank.ACE]


@dataclass(frozen=True, slots=True)
class FiveHundredDeck(Deck[FiveHundredCard]):
    @staticmethod
    @override
    def build(shuffled: bool = True) -> "FiveHundredDeck":
        deck = FiveHundredDeck([FiveHundredCard(suit=suit, rank=rank) for suit in Suit for rank in RANKS])
        if shuffled:
            deck._shuffle()
        return deck

    @staticmethod
    @override
    def from_card_strings(card_strings: list[str], shuffled: bool = True) -> "FiveHundredDeck":
        deck = FiveHundredDeck([FiveHundredCard.from_string(card_str) for card_str in card_strings])
        if shuffled:
            deck._shuffle()
        return deck

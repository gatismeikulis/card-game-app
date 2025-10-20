from dataclasses import dataclass
from typing import Self, override

from ...common.card import Rank, Suit
from ...common.deck import Deck
from .five_hundred_card import FiveHundredCard

# Game 'Five Hundred' only uses 24 card deck, from 9 to Ace of each suit
RANKS = [Rank.NINE, Rank.JACK, Rank.QUEEN, Rank.KING, Rank.TEN, Rank.ACE]


@dataclass(frozen=True, slots=True)
class FiveHundredDeck(Deck[FiveHundredCard]):
    @classmethod
    @override
    def build(cls) -> Self:
        return cls([FiveHundredCard(suit=suit, rank=rank) for suit in Suit for rank in RANKS])

    @classmethod
    @override
    def from_card_strings(cls, card_strings: list[str]) -> Self:
        return cls(shuffled=False, _cards=[FiveHundredCard.from_string(card_str) for card_str in card_strings])

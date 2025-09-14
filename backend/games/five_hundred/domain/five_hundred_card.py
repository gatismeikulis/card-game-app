from dataclasses import dataclass
from enum import Enum
from typing import override
from ...common.card import Card, Rank, Strength


class CardPoints(Enum):
    NINE = 0
    JACK = 2
    QUEEN = 3
    KING = 4
    TEN = 10
    ACE = 11


RANK_TO_VALUE: dict[Rank, CardPoints] = {
    Rank.NINE: CardPoints.NINE,
    Rank.JACK: CardPoints.JACK,
    Rank.QUEEN: CardPoints.QUEEN,
    Rank.KING: CardPoints.KING,
    Rank.TEN: CardPoints.TEN,
    Rank.ACE: CardPoints.ACE,
}

RANK_TO_STRENGTH: dict[Rank, Strength] = {
    Rank.NINE: Strength.ONE,
    Rank.JACK: Strength.TWO,
    Rank.QUEEN: Strength.THREE,
    Rank.KING: Strength.FOUR,
    Rank.TEN: Strength.FIVE,
    Rank.ACE: Strength.SIX,
}

# 'frozen = True' makes the class immutable meaning that the attributes cannot be changed after the object is created
# 'slots = True' is a performance optimization that replaces the __dict__ attribute with a slots attribute
# meaning that the attributes are stored in a tuple instead of a dictionary.


@dataclass(slots=True, frozen=True, repr=False)
class FiveHundredCard(Card):
    @property
    def points(self) -> CardPoints:
        return RANK_TO_VALUE[self.rank]

    @override
    def strength(self) -> Strength:
        return RANK_TO_STRENGTH[self.rank]

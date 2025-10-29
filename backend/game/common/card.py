from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
from typing import Self, override

from .game_exception import GameParsingException


class Suit(Enum):
    HEART = ("Heart", "h")
    DIAMOND = ("Diamond", "d")
    CLUB = ("Club", "c")
    SPADE = ("Spade", "s")

    def __init__(self, full_name: str, symbol: str):
        self.full_name = full_name
        self.symbol = symbol

    @staticmethod
    def from_string(symbol: str) -> "Suit":
        match symbol.upper():
            case "H":
                return Suit.HEART
            case "D":
                return Suit.DIAMOND
            case "C":
                return Suit.CLUB
            case "S":
                return Suit.SPADE
            case _:
                raise GameParsingException(
                    reason="card_suit_parsing_error", detail=f"Could not parse card's suit from input: {symbol}"
                )

    @override
    def __str__(self) -> str:
        return f"{SUIT_COLORS[self]}{self.full_name}\033[0m"

    @override
    def __repr__(self) -> str:
        return self.__str__()


class Rank(Enum):
    ACE = ("Ace", "A")
    TWO = ("Two", "2")
    THREE = ("Three", "3")
    FOUR = ("Four", "4")
    FIVE = ("Five", "5")
    SIX = ("Six", "6")
    SEVEN = ("Seven", "7")
    EIGHT = ("Eight", "8")
    NINE = ("Nine", "9")
    TEN = ("Ten", "T")
    JACK = ("Jack", "J")
    QUEEN = ("Queen", "Q")
    KING = ("King", "K")

    def __init__(self, full_name: str, symbol: str):
        self.full_name = full_name
        self.symbol = symbol

    @staticmethod
    def from_string(symbol: str) -> "Rank":
        match symbol.upper():
            case "A":
                return Rank.ACE
            case "2":
                return Rank.TWO
            case "3":
                return Rank.THREE
            case "4":
                return Rank.FOUR
            case "5":
                return Rank.FIVE
            case "6":
                return Rank.SIX
            case "7":
                return Rank.SEVEN
            case "8":
                return Rank.EIGHT
            case "9":
                return Rank.NINE
            case "T":
                return Rank.TEN
            case "J":
                return Rank.JACK
            case "Q":
                return Rank.QUEEN
            case "K":
                return Rank.KING
            case _:
                raise GameParsingException(
                    reason="card_rank_parsing_error", detail=f"Could not parse card's rank from input: {symbol}"
                )


class Strength(Enum):
    ONE = auto()
    TWO = auto()
    THREE = auto()
    FOUR = auto()
    FIVE = auto()
    SIX = auto()


SUIT_COLORS = {
    Suit.HEART: "\033[91m",  # Red
    Suit.DIAMOND: "\033[94m",  # Blue
    Suit.CLUB: "\033[92m",  # Green
    Suit.SPADE: "\033[97m",  # White
}


@dataclass(frozen=True, slots=True)
class Card(ABC):
    suit: Suit
    rank: Rank

    @classmethod
    def from_string(cls, card_str: str) -> Self:
        """Create a card from string representation. Format is 'rank' + 'suit'. E.g. 'Ah', '2D', 'Tc'."""
        rank = Rank.from_string(card_str[0])
        suit = Suit.from_string(card_str[1])
        return cls(suit=suit, rank=rank)

    @abstractmethod
    def strength(self) -> Strength: ...

    def to_dict(self) -> str:
        """Serialize to JSON-compatible string"""
        return f"{self.rank.symbol}{self.suit.symbol}"

    @classmethod
    def from_dict(cls, data: str) -> Self:
        """Reconstruct from JSON-compatible string"""
        return cls.from_string(data)

    @override
    def __str__(self) -> str:
        return f"{SUIT_COLORS[self.suit]}{self.rank.symbol}{self.suit.symbol}\033[0m"

    @override
    def __repr__(self) -> str:
        return self.__str__()

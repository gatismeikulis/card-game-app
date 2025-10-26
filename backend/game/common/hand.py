from abc import ABC
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Generic, Self, TypeVar, override

from .game_exception import GameEngineException
from .card import Card

TCard = TypeVar("TCard", bound=Card)


@dataclass(frozen=True, slots=True)
class Hand(ABC, Generic[TCard]):
    cards: tuple[TCard, ...]

    def __post_init__(self) -> None:
        # Sort cards on construction (frozen dataclass workaround)
        sorted_cards = tuple(sorted(self.cards, key=lambda card: (card.suit.symbol, -card.strength().value)))
        object.__setattr__(self, "cards", sorted_cards)

    def with_added_cards(self, cards: Sequence[TCard]) -> Self:
        return type(self)(self.cards + tuple(cards))

    def without_cards(self, cards: Sequence[TCard]) -> Self:
        for c in cards:
            if c not in self.cards:
                raise GameEngineException(
                    reason="card_not_in_hand",
                    message=f"Could not remove card from hand: card {c} is not in the hand {self.cards}",
                )
        result: list[TCard] = []
        for c in self.cards:
            if c not in cards:
                result.append(c)
        return type(self)(tuple(result))

    def to_dict(self) -> list[str]:
        """Serialize to JSON-compatible list of strings"""
        return [card.to_dict() for card in self.cards]

    @classmethod
    def from_dict(cls, data: list[str], card_class: type[TCard]) -> Self:
        """Reconstruct from JSON-compatible list of strings"""
        return cls(tuple(card_class.from_dict(card) for card in data))

    @override
    def __str__(self) -> str:
        return f"{' '.join(str(card) for card in self.cards)}"

    @override
    def __repr__(self) -> str:
        return self.__str__()

from abc import ABC, abstractmethod
from collections.abc import Sequence
from dataclasses import dataclass, field
from random import shuffle
from typing import Generic, Self, TypeVar, override

from .card import Card

TCard = TypeVar("TCard", bound=Card)


@dataclass(frozen=True, slots=True)
class Deck(ABC, Generic[TCard]):
    _cards: list[TCard]
    shuffled: bool = True  # if True, the deck is shuffled when it is initialized
    _undealed_deck: Sequence[TCard] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.shuffled:
            shuffle(self._cards)
        object.__setattr__(self, "_undealed_deck", self._cards.copy())

    def draw_one(self) -> TCard:
        return self._cards.pop()

    def draw_many(self, count: int) -> list[TCard]:
        take = min(max(count, 0), len(self._cards))
        dealt = self._cards[-take:]
        del self._cards[-take:]
        return dealt

    @classmethod
    @abstractmethod
    def build(cls) -> Self: ...

    @classmethod
    @abstractmethod
    def from_card_strings(cls, card_strings: list[str]) -> Self: ...

    def to_dict(self) -> list[str]:
        return [card.to_dict() for card in self._undealed_deck]

    @classmethod
    def from_dict(cls, data: list[str], card_class: type[TCard]) -> Self:
        """Reconstruct from JSON-compatible list of strings"""
        return cls([card_class.from_dict(card) for card in data], shuffled=False)

    @override
    def __str__(self) -> str:
        return f"{' '.join(str(card) for card in self._cards)}"

    @override
    def __repr__(self) -> str:
        return self.__str__()

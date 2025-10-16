from abc import ABC, abstractmethod
from dataclasses import dataclass
from random import shuffle
from typing import Generic, TypeVar

from .card import Card

TCard = TypeVar("TCard", bound=Card)


@dataclass(frozen=True, slots=True)
class Deck(ABC, Generic[TCard]):
    _cards: list[TCard]

    def _shuffle(self) -> None:
        shuffle(self._cards)

    def draw_one(self) -> TCard:
        return self._cards.pop()

    def draw_many(self, count: int) -> list[TCard]:
        take = min(max(count, 0), len(self._cards))
        dealt = self._cards[-take:]
        del self._cards[-take:]
        return dealt

    @staticmethod
    @abstractmethod
    def build(shuffled: bool = False) -> "Deck[TCard]": ...

    @staticmethod
    @abstractmethod
    def from_card_strings(card_strings: list[str], shuffled: bool = False) -> "Deck[TCard]": ...

from __future__ import annotations
from dataclasses import dataclass
from typing import Generic, Self, TypeVar, override
from abc import ABC
from collections.abc import Sequence

from .card import Card

TCard = TypeVar("TCard", bound=Card)


@dataclass(frozen=True, slots=True)
class Hand(ABC, Generic[TCard]):
    _cards: list[TCard]

    @property
    def cards(self) -> Sequence[TCard]:
        return self._cards

    def with_added_cards(self, cards: Sequence[TCard]) -> Self:
        return type(self)(self._cards + list(cards))

    def without_cards(self, cards: Sequence[TCard]) -> Self:
        for c in cards:
            if c not in self._cards:
                raise ValueError(f"Card {c} is not in the hand {self._cards}")
        result: Sequence[TCard] = []
        for c in self._cards:
            if c not in cards:
                result.append(c)
        return type(self)(result)

    @override
    def __str__(self) -> str:
        return f"{sorted(self._cards, key=lambda card: (card.suit.symbol, -card.strength().value))}"

    @override
    def __repr__(self) -> str:
        return self.__str__()

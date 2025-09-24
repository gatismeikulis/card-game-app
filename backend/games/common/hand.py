from __future__ import annotations

from abc import ABC
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Generic, Self, TypeVar, override

from .card import Card

TCard = TypeVar("TCard", bound=Card)


@dataclass(frozen=True, slots=True)
class Hand(ABC, Generic[TCard]):
    cards: tuple[TCard, ...]

    def with_added_cards(self, cards: Sequence[TCard]) -> Self:
        return type(self)(self.cards + tuple(cards))

    def without_cards(self, cards: Sequence[TCard]) -> Self:
        for c in cards:
            if c not in self.cards:
                raise ValueError(f"Card {c} is not in the hand {self.cards}")
        result: list[TCard] = []
        for c in self.cards:
            if c not in cards:
                result.append(c)
        return type(self)(tuple(result))

    @override
    def __str__(self) -> str:
        return f"{sorted(self.cards, key=lambda card: (card.suit.symbol, -card.strength().value))}"

    @override
    def __repr__(self) -> str:
        return self.__str__()

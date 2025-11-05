from collections.abc import Sequence
from dataclasses import dataclass
from typing import ClassVar, Literal, Any, Self, override

from ...common.game_event import GameEvent
from ...common.seat import Seat
from .five_hundred_deck import FiveHundredDeck
from .five_hundred_card import FiveHundredCard


@dataclass(frozen=True, slots=True)
class DeckShuffledEvent(GameEvent):
    type: ClassVar[Literal["deck_shuffled"]] = "deck_shuffled"
    deck: FiveHundredDeck

    @override
    def to_dict(self) -> dict[str, Any]:
        return {
            "type": self.type,
            "deck": self.deck.to_dict(),
        }

    @classmethod
    @override
    def from_dict(cls, data: dict[str, Any]) -> Self:
        return cls(
            deck=FiveHundredDeck.from_dict(data["deck"], FiveHundredCard),
        )


@dataclass(frozen=True, slots=True)
class BidMadeEvent(GameEvent):
    type: ClassVar[Literal["bid_made"]] = "bid_made"
    bid: int
    made_by: Seat

    @override
    def to_dict(self) -> dict[str, Any]:
        return {
            "type": self.type,
            "bid": self.bid,
            "made_by": self.made_by.to_dict(),
        }

    @classmethod
    @override
    def from_dict(cls, data: dict[str, Any]) -> Self:
        return cls(
            bid=data["bid"],
            made_by=Seat.from_dict(data["made_by"]),
        )


@dataclass(frozen=True, slots=True)
class BiddingFinishedEvent(GameEvent):
    type: ClassVar[Literal["bidding_finished"]] = "bidding_finished"
    bid: int | None
    made_by: Seat | None

    @override
    def to_dict(self) -> dict[str, Any]:
        return {"type": self.type, "bid": self.bid, "made_by": self.made_by.to_dict() if self.made_by else None}

    @classmethod
    @override
    def from_dict(cls, data: dict[str, Any]) -> Self:
        return cls(
            bid=data["bid"],
            made_by=Seat.from_dict(data["made_by"]) if data["made_by"] else None,
        )


@dataclass(frozen=True, slots=True)
class HiddenCardsTakenEvent(GameEvent):
    type: ClassVar[Literal["hidden_cards_taken"]] = "hidden_cards_taken"

    @override
    def to_dict(self) -> dict[str, Any]:
        return {"type": self.type}

    @classmethod
    @override
    def from_dict(cls, data: dict[str, Any]) -> Self:
        return cls()


@dataclass(frozen=True, slots=True)
class DeclarerGaveUpEvent(GameEvent):
    type: ClassVar[Literal["declarer_gave_up"]] = "declarer_gave_up"
    made_by: Seat

    @override
    def to_dict(self) -> dict[str, Any]:
        return {"type": self.type, "made_by": self.made_by.to_dict()}

    @classmethod
    @override
    def from_dict(cls, data: dict[str, Any]) -> Self:
        return cls(made_by=Seat.from_dict(data["made_by"]))


@dataclass(frozen=True, slots=True)
class CardsPassedEvent(GameEvent):
    type: ClassVar[Literal["cards_passed"]] = "cards_passed"
    card_to_next_seat: FiveHundredCard
    card_to_prev_seat: FiveHundredCard

    @override
    def to_dict(self) -> dict[str, Any]:
        return {
            "type": self.type,
            "card_to_next_seat": self.card_to_next_seat.to_dict(),
            "card_to_prev_seat": self.card_to_prev_seat.to_dict(),
        }

    @classmethod
    @override
    def from_dict(cls, data: dict[str, Any]) -> Self:
        return cls(
            card_to_next_seat=FiveHundredCard.from_dict(data["card_to_next_seat"]),
            card_to_prev_seat=FiveHundredCard.from_dict(data["card_to_prev_seat"]),
        )


@dataclass(frozen=True, slots=True)
class CardPlayedEvent(GameEvent):
    type: ClassVar[Literal["card_played"]] = "card_played"
    card: FiveHundredCard
    played_by: Seat

    @override
    def to_dict(self) -> dict[str, Any]:
        return {
            "type": self.type,
            "card": self.card.to_dict(),
            "played_by": self.played_by.to_dict(),
        }

    @classmethod
    @override
    def from_dict(cls, data: dict[str, Any]) -> Self:
        return cls(
            card=FiveHundredCard.from_dict(data["card"]),
            played_by=Seat.from_dict(data["played_by"]),
        )


@dataclass(frozen=True, slots=True)
class MarriagePointsAddedEvent(GameEvent):
    type: ClassVar[Literal["marriage_points_added"]] = "marriage_points_added"
    points: int
    added_to: Seat

    @override
    def to_dict(self) -> dict[str, Any]:
        return {
            "type": self.type,
            "points": self.points,
            "added_to": self.added_to.to_dict(),
        }

    @classmethod
    @override
    def from_dict(cls, data: dict[str, Any]) -> Self:
        return cls(
            points=data["points"],
            added_to=Seat.from_dict(data["added_to"]),
        )


@dataclass(frozen=True, slots=True)
class TrickTakenEvent(GameEvent):
    type: ClassVar[Literal["trick_taken"]] = "trick_taken"
    taken_by: Seat
    cards: Sequence[FiveHundredCard]

    @override
    def to_dict(self) -> dict[str, Any]:
        return {
            "type": self.type,
            "taken_by": self.taken_by.to_dict(),
            "cards": [card.to_dict() for card in self.cards],
        }

    @classmethod
    @override
    def from_dict(cls, data: dict[str, Any]) -> Self:
        return cls(
            taken_by=Seat.from_dict(data["taken_by"]),
            cards=[FiveHundredCard.from_dict(card_data) for card_data in data["cards"]],
        )


@dataclass(frozen=True, slots=True)
class RoundFinishedEvent(GameEvent):
    type: ClassVar[Literal["round_finished"]] = "round_finished"
    round_number: int
    declarer: Seat | None
    given_up: bool

    @override
    def to_dict(self) -> dict[str, Any]:
        return {
            "type": self.type,
            "round_number": self.round_number,
            "declarer": self.declarer.to_dict() if self.declarer else None,
            "given_up": self.given_up,
        }

    @classmethod
    @override
    def from_dict(cls, data: dict[str, Any]) -> Self:
        return cls(
            round_number=data["round_number"],
            declarer=Seat.from_dict(data["declarer"]) if data["declarer"] else None,
            given_up=data["given_up"],
        )


@dataclass(frozen=True, slots=True)
class GameFinishedEvent(GameEvent):
    type: ClassVar[Literal["game_finished"]] = "game_finished"

    @override
    def to_dict(self) -> dict[str, Any]:
        return {"type": self.type}

    @classmethod
    @override
    def from_dict(cls, data: dict[str, Any]) -> Self:
        return cls()


FiveHundredEvent = (
    DeckShuffledEvent
    | BidMadeEvent
    | BiddingFinishedEvent
    | HiddenCardsTakenEvent
    | DeclarerGaveUpEvent
    | CardsPassedEvent
    | CardPlayedEvent
    | RoundFinishedEvent
    | GameFinishedEvent
    | MarriagePointsAddedEvent
    | TrickTakenEvent
)

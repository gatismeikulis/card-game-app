from typing import Any
from ..five_hundred_event import (
    CardPlayedEvent,
    DeckShuffledEvent,
    BidMadeEvent,
    BiddingFinishedEvent,
    FiveHundredEvent,
    GameFinishedEvent,
    HiddenCardsTakenEvent,
    CardsPassedEvent,
    MarriagePointsAddedEvent,
    RoundFinishedEvent,
    TrickTakenEvent,
)
from ..five_hundred_card import FiveHundredCard
from ..five_hundred_deck import FiveHundredDeck
from ....common.card import Suit, Rank
from ....common.seat import Seat
import pytest


@pytest.mark.parametrize(
    "event_class, kwargs",
    [
        (DeckShuffledEvent, {"deck": FiveHundredDeck.from_card_strings(["9H", "JH", "QH", "KH", "TH", "AH"])}),
        (BidMadeEvent, {"bid": 100, "made_by": Seat(1)}),
        (BiddingFinishedEvent, {"bid": None, "made_by": None}),
        (BiddingFinishedEvent, {"bid": 100, "made_by": Seat(1)}),
        (HiddenCardsTakenEvent, {}),
        (
            CardsPassedEvent,
            {
                "card_to_next_seat": FiveHundredCard(Suit.HEART, Rank.ACE),
                "card_to_prev_seat": FiveHundredCard(Suit.CLUB, Rank.KING),
            },
        ),
        (CardPlayedEvent, {"card": FiveHundredCard(Suit.DIAMOND, Rank.QUEEN), "played_by": Seat(2)}),
        (MarriagePointsAddedEvent, {"points": 10, "added_to": Seat(3)}),
        (
            TrickTakenEvent,
            {
                "taken_by": Seat(4),
                "cards": [FiveHundredCard(Suit.SPADE, Rank.JACK), FiveHundredCard(Suit.CLUB, Rank.TEN)],
            },
        ),
        (RoundFinishedEvent, {"round_number": 1}),
        (GameFinishedEvent, {}),
    ],
)
def test_event_to_dict_from_dict_roundtrip(event_class: type[FiveHundredEvent], kwargs: dict[str, Any]):
    event = event_class(**kwargs)
    data = event.to_dict()
    restored = event_class.from_dict(data)
    assert restored == event

from typing import Any
from ..five_hundred_event import (
    CardPlayedEvent,
    DeckShuffledEvent,
    BidMadeEvent,
    BiddingFinishedEvent,
    FiveHundredEvent,
    GameEndedEvent,
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
    argnames="event_class, kwargs",
    argvalues=[
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
        (RoundFinishedEvent, {"round_number": 1, "declarer": Seat(1), "given_up": False}),
        (RoundFinishedEvent, {"round_number": 3, "declarer": None, "given_up": True}),
        (RoundFinishedEvent, {"round_number": 3, "declarer": None, "given_up": False}),
        (GameEndedEvent, {}),
    ],
    ids=[
        "deck_shuffled",
        "bid_made",
        "bidding_finished_no_bids",
        "bidding_finished_with_bid",
        "hidden_cards_taken",
        "cards_passed",
        "card_played",
        "marriage_points_added",
        "trick_taken",
        "round_finished_has_declarer",
        "round_finished_declarer_gave_up",
        "round_finished_no_declarer",
        "game_ended",
    ],
)
def test_event_to_dict_from_dict_roundtrip(event_class: type[FiveHundredEvent], kwargs: dict[str, Any]):
    event = event_class(**kwargs)
    data = event.to_dict()
    restored = event_class.from_dict(data)
    assert restored == event

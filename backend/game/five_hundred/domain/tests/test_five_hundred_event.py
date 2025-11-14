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
from ....common.game_ending import GameEndingReason
import pytest


@pytest.mark.parametrize(
    argnames="event_class, kwargs",
    argvalues=[
        (
            DeckShuffledEvent,
            {"deck": FiveHundredDeck.from_card_strings(["9H", "JH", "QH", "KH", "TH", "AH"]), "seq_number": 1},
        ),
        (BidMadeEvent, {"bid": 100, "made_by": Seat(1), "seq_number": 1}),
        (BiddingFinishedEvent, {"bid": None, "made_by": None, "seq_number": 1}),
        (BiddingFinishedEvent, {"bid": 100, "made_by": Seat(1), "seq_number": 1}),
        (HiddenCardsTakenEvent, {"seq_number": 1}),
        (
            CardsPassedEvent,
            {
                "card_to_next_seat": FiveHundredCard(Suit.HEART, Rank.ACE),
                "card_to_prev_seat": FiveHundredCard(Suit.CLUB, Rank.KING),
                "seq_number": 1,
            },
        ),
        (CardPlayedEvent, {"card": FiveHundredCard(Suit.DIAMOND, Rank.QUEEN), "played_by": Seat(2), "seq_number": 1}),
        (MarriagePointsAddedEvent, {"points": 10, "added_to": Seat(3), "seq_number": 1}),
        (
            TrickTakenEvent,
            {
                "taken_by": Seat(4),
                "cards": [FiveHundredCard(Suit.SPADE, Rank.JACK), FiveHundredCard(Suit.CLUB, Rank.TEN)],
                "seq_number": 1,
            },
        ),
        (
            RoundFinishedEvent,
            {
                "round_number": 1,
                "declarer": Seat(1),
                "given_up": False,
                "points": {Seat(1): 100, Seat(2): -35, Seat(3): 15},
                "seq_number": 1,
            },
        ),
        (
            RoundFinishedEvent,
            {
                "round_number": 3,
                "declarer": Seat(1),
                "given_up": True,
                "points": {Seat(1): 120, Seat(2): -50, Seat(3): -50},
                "seq_number": 1,
            },
        ),
        (
            RoundFinishedEvent,
            {
                "round_number": 3,
                "declarer": None,
                "given_up": False,
                "points": {Seat(1): 0, Seat(2): 0, Seat(3): 0},
                "seq_number": 1,
            },
        ),
        (GameEndedEvent, {"reason": GameEndingReason.FINISHED, "seat": None, "seq_number": 1}),
        (GameEndedEvent, {"reason": GameEndingReason.ABORTED, "seat": Seat(2), "seq_number": 1}),
        (GameEndedEvent, {"reason": GameEndingReason.CANCELLED, "seat": None, "seq_number": 1}),
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
        "game_ended_finished",
        "game_ended_aborted",
        "game_ended_cancelled",
    ],
)
def test_event_to_dict_from_dict_roundtrip(event_class: type[FiveHundredEvent], kwargs: dict[str, Any]):
    event = event_class(**kwargs)
    data = event.to_dict()
    restored = event_class.from_dict(data)
    assert restored == event

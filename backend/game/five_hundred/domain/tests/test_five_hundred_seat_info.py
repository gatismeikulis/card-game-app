import pytest

from ..five_hundred_seat_info import FiveHundredSeatInfo
from ..five_hundred_card import FiveHundredCard
from ....common.card import Suit, Rank
from ....common.hand import Hand


Ah = FiveHundredCard(Suit.HEART, Rank.ACE)
Kh = FiveHundredCard(Suit.HEART, Rank.KING)
Ts = FiveHundredCard(Suit.SPADE, Rank.TEN)
Js = FiveHundredCard(Suit.SPADE, Rank.JACK)
Qs = FiveHundredCard(Suit.SPADE, Rank.QUEEN)


@pytest.fixture
def sample_seat_info() -> FiveHundredSeatInfo:
    return FiveHundredSeatInfo(
        hand=Hand[FiveHundredCard](tuple([Ah, Kh, Ts, Js, Qs])),
        bid=120,
        points=11,
        trick_count=2,
        marriage_points=[40],
    )


@pytest.mark.parametrize(
    argnames="required_suit, trump_suit, expected_cards",
    argvalues=[
        (None, None, {Ah, Kh, Ts, Js, Qs}),
        (None, Suit.CLUB, {Ah, Kh, Ts, Js, Qs}),
        (Suit.SPADE, Suit.SPADE, {Ts, Js, Qs}),
        (Suit.HEART, Suit.DIAMOND, {Ah, Kh}),
        (Suit.DIAMOND, Suit.SPADE, {Qs, Js, Ts}),
        (Suit.CLUB, Suit.DIAMOND, {Ah, Kh, Ts, Js, Qs}),
    ],
    ids=[
        "suit_not_required_trump_not_set",
        "suit_not_required_trump_is_set",
        "required_suit_and_trump_in_hand",
        "required_suit_in_hand_but_no_trump",
        "no_required_suit_but_has_trump_in_hand",
        "no_required_suit_no_trump_in_hand",
    ],
)
def test_cards_allowed_to_play_no_required_or_trump(
    sample_seat_info: FiveHundredSeatInfo,
    required_suit: Suit | None,
    trump_suit: Suit | None,
    expected_cards: set[FiveHundredCard],
):
    cards_allowed_to_play = sample_seat_info.cards_allowed_to_play(required_suit, trump_suit)
    assert set(cards_allowed_to_play) == expected_cards


def test_to_dict_and_from_dict_roundtrip(sample_seat_info: FiveHundredSeatInfo):
    data = sample_seat_info.to_dict()
    restored = FiveHundredSeatInfo.from_dict(data)
    assert restored == sample_seat_info


def test_to_public_dict_hides_private_info(sample_seat_info: FiveHundredSeatInfo):
    public_data = sample_seat_info.to_public_dict()
    assert public_data["hand"] == len(sample_seat_info.hand.cards)
    assert public_data["points"] is None
    assert public_data["marriage_points"] is None
    assert public_data["bid"] == 120
    assert public_data["trick_count"] == 2

import pytest
from typing import override
from ..card import Card, Suit, Rank, Strength
from ..hand import Hand
from ..game_exception import GameEngineException


class DummyCard(Card):
    @override
    def strength(self) -> Strength:
        return Strength.ONE  # sorting uses strength() value


card1 = DummyCard(Suit.HEART, Rank.ACE)
card2 = DummyCard(Suit.DIAMOND, Rank.TWO)
card3 = DummyCard(Suit.CLUB, Rank.THREE)
card4 = DummyCard(Suit.SPADE, Rank.FOUR)
card5 = DummyCard(Suit.HEART, Rank.KING)


@pytest.fixture
def dummy_hand() -> Hand[DummyCard]:
    return Hand((card1, card2, card3, card4))  # unsorted input


def test_hand_sorts_on_construction(dummy_hand: Hand[DummyCard]):
    # Expected sorted by suit, then -strength()
    expected = (card3, card2, card1, card4)
    assert dummy_hand.cards == expected


def test_with_added_cards(dummy_hand: Hand[DummyCard]):
    new_hand = dummy_hand.with_added_cards([card5])
    assert card5 in new_hand.cards
    assert all(c in new_hand.cards for c in dummy_hand.cards)
    assert len(new_hand.cards) == len(dummy_hand.cards) + 1


def test_without_cards_valid(dummy_hand: Hand[DummyCard]):
    new_hand = dummy_hand.without_cards([card2, card3])
    assert card2 not in new_hand.cards
    assert card3 not in new_hand.cards
    assert len(new_hand.cards) == 2


def test_without_cards_invalid(dummy_hand: Hand[DummyCard]):
    with pytest.raises(GameEngineException):
        _ = dummy_hand.without_cards([card5])


def test_to_dict_and_from_dict_roundtrip(dummy_hand: Hand[DummyCard]):
    data = dummy_hand.to_dict()
    restored = Hand.from_dict(data, DummyCard)
    assert restored == dummy_hand

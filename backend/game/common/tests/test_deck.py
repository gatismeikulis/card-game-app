import pytest
from unittest.mock import Mock
from typing import override, Self
from ..card import Card, Rank, Suit, Strength
from ..deck import Deck


class DummyCard(Card):
    @override
    def strength(self) -> Strength: ...


class DummyDeck(Deck[DummyCard]):
    @classmethod
    @override
    def build(cls) -> Self: ...

    @classmethod
    @override
    def from_card_strings(cls, card_strings: list[str]) -> Self: ...


card1 = DummyCard(Suit.HEART, Rank.ACE)
card2 = DummyCard(Suit.DIAMOND, Rank.TWO)
card3 = DummyCard(Suit.CLUB, Rank.THREE)
card4 = DummyCard(Suit.SPADE, Rank.FOUR)

cards = [card1, card2, card3, card4]


@pytest.fixture
def dummy_deck() -> DummyDeck:
    """Fixture that creates a fresh deck for each test"""
    return DummyDeck(_cards=cards.copy(), shuffle_on_init=False)


def test_initial_deck_order_is_persisted(dummy_deck: DummyDeck):
    assert dummy_deck._undealed_deck == cards


def test_deck_draw_one_and_many(dummy_deck: DummyDeck):
    # deck is supposed to draw starting from last card (top of the deck card)
    first_card = dummy_deck.draw_one()
    assert first_card == card4

    next_two_cards = dummy_deck.draw_many(2)
    assert next_two_cards == [card2, card3]


def test_draw_many_more_than_available(dummy_deck: DummyDeck):
    drawn = dummy_deck.draw_many(10)  # ask more than deck size
    assert len(drawn) == 4
    assert len(dummy_deck._cards) == 0  # deck is empty


def test_from_dict_and_to_dict_roundtrip(dummy_deck: DummyDeck):
    data = dummy_deck.to_dict()
    new_deck = DummyDeck.from_dict(data, DummyCard)
    assert new_deck.to_dict() == dummy_deck.to_dict()


def test_shuffle_called_on_init():
    mock_shuffle = Mock()
    _ = DummyDeck(_cards=cards.copy(), shuffle_on_init=True, shuffle_fn=mock_shuffle)
    assert mock_shuffle.call_count == 1

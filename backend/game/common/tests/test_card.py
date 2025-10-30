from typing import override
import pytest

from ..card import Suit, Rank, Card, Strength
from ..game_exception import GameParsingException


@pytest.mark.parametrize(
    "symbol,expected",
    [
        ("c", Suit.CLUB),
        ("D", Suit.DIAMOND),
        ("h", Suit.HEART),
        ("S", Suit.SPADE),
    ],
)
def test_suit_from_string_valid(symbol: str, expected: Suit):
    assert Suit.from_string(symbol) == expected


def test_suit_from_string_invalid():
    with pytest.raises(GameParsingException) as exc:
        _ = Suit.from_string("x")
    assert "card_suit_parsing_error" in exc.value.reason


@pytest.mark.parametrize(
    "symbol,expected",
    [
        ("A", Rank.ACE),
        ("2", Rank.TWO),
        ("T", Rank.TEN),
        ("k", Rank.KING),
    ],
)
def test_rank_from_string_valid(symbol: str, expected: Rank):
    assert Rank.from_string(symbol) == expected


def test_rank_from_string_invalid():
    with pytest.raises(GameParsingException) as exc:
        _ = Rank.from_string("Z")
    assert "card_rank_parsing_error" in exc.value.reason


class DummyCard(Card):
    @override
    def strength(self) -> Strength:
        return Strength.ONE


def test_card_from_string_and_to_dict_roundtrip():
    card = DummyCard.from_string("Ah")
    assert card.rank == Rank.ACE
    assert card.suit == Suit.HEART

    serialized = card.to_dict()
    assert serialized == "Ah"

    deserialized = DummyCard.from_dict(serialized)
    assert deserialized == card


def test_card_from_string_invalid():
    with pytest.raises(GameParsingException):
        _ = DummyCard.from_string("AB")

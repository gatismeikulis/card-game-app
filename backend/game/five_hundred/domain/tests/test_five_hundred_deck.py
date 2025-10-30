from ..five_hundred_deck import FiveHundredDeck
from ....common.card import Suit, Rank


def test_build_deck_has_24_cards():
    deck = FiveHundredDeck.build()
    assert len(deck._cards) == 24

    # all suits present
    suits = {card.suit for card in deck._cards}
    assert suits == set(Suit)

    # only allowed ranks present
    ranks = {card.rank for card in deck._cards}
    assert ranks == {Rank.NINE, Rank.JACK, Rank.QUEEN, Rank.KING, Rank.TEN, Rank.ACE}

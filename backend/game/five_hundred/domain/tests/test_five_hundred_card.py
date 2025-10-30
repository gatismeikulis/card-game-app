from ..five_hundred_card import RANK_TO_VALUE, RANK_TO_STRENGTH, FiveHundredCard
from ....common.card import Suit


def test_card_points_mapping_is_consistent():
    for rank, expected_points in RANK_TO_VALUE.items():
        card = FiveHundredCard(Suit.HEART, rank)
        assert card.points == expected_points


def test_card_strength_mapping_is_consistent():
    for rank, expected_strength in RANK_TO_STRENGTH.items():
        card = FiveHundredCard(Suit.SPADE, rank)
        assert card.strength() == expected_strength

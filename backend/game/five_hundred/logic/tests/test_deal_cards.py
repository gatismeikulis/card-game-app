from ...domain.five_hundred_phase import FiveHundredPhase
from ...domain.constants import CARDS_IN_STARTING_HAND, CARDS_TO_TAKE
from ...domain.five_hundred_deck import FiveHundredDeck
from ....common.seat import Seat
from ..deal_cards import deal_cards
from ...domain.five_hundred_game import FiveHundredGame


def test_deal_cards_logic(sample_game: FiveHundredGame):
    deck = FiveHundredDeck.build()
    game = deal_cards(sample_game, deck)

    assert len(game.round.cards_to_take) == CARDS_TO_TAKE
    assert len(game.round.seat_infos[Seat(1)].hand.cards) == CARDS_IN_STARTING_HAND
    assert game.round.phase == FiveHundredPhase.BIDDING

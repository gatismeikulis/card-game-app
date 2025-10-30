from ..take_hidden_cards import take_hidden_cards
from ...domain.five_hundred_game import FiveHundredGame


def test_take_hidden_cards_logic(sample_game: FiveHundredGame):
    game = take_hidden_cards(sample_game)

    assert game.round.seat_infos[sample_game.active_seat].hand == sample_game.round.seat_infos[
        sample_game.active_seat
    ].hand.with_added_cards(sample_game.round.cards_to_take)
    assert game.round.cards_to_take == []

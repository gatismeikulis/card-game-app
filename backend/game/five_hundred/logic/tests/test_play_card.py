from dataclasses import replace
from ....common.card import Rank, Suit
from ...domain.five_hundred_card import FiveHundredCard
from ...domain.five_hundred_game import FiveHundredGame
from ..play_card import play_card


def test_play_first_card_sets_required_and_trump_suit(sample_game: FiveHundredGame):
    card_to_play = FiveHundredCard(Suit.CLUB, Rank.ACE)
    sample_round = sample_game.round
    sample_active_seats_info = sample_game.active_seats_info
    sample_active_seats_info_updated = replace(
        sample_active_seats_info, hand=sample_active_seats_info.hand.with_added_cards([card_to_play])
    )
    sample_round_updated = replace(sample_round, seat_infos={sample_game.active_seat: sample_active_seats_info_updated})
    sample_game_updated = replace(sample_game, round=sample_round_updated)

    game = play_card(sample_game_updated, card=card_to_play)

    # Required and trump suits should now be set
    assert game.round.required_suit == card_to_play.suit
    assert game.round.trump_suit == card_to_play.suit

    # Card should be on the board mapped to the active seat
    assert game.round.cards_on_board[sample_game.active_seat] == card_to_play

    # That card should be removed from hand
    assert card_to_play not in game.round.seat_infos[sample_game.active_seat].hand.cards

    # Active seat should move to the next player
    assert game.active_seat == sample_game.active_seat.next(sample_game.taken_seats)

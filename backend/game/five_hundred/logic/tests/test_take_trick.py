from dataclasses import replace

from ....common.card import Rank, Suit
from ....common.seat import Seat
from ...domain.five_hundred_card import FiveHundredCard
from ...domain.five_hundred_game import FiveHundredGame
from ..take_trick import take_trick


def test_take_trick_logic(sample_game: FiveHundredGame):
    tricks_before = [
        {
            Seat(1): FiveHundredCard(Suit.DIAMOND, Rank.JACK),
            Seat(2): FiveHundredCard(Suit.DIAMOND, Rank.NINE),
            Seat(3): FiveHundredCard(Suit.DIAMOND, Rank.KING),
        }
    ]
    cards_on_board = {
        Seat(1): FiveHundredCard(Suit.CLUB, Rank.KING),
        Seat(2): FiveHundredCard(Suit.CLUB, Rank.NINE),
        Seat(3): FiveHundredCard(Suit.CLUB, Rank.ACE),
    }
    round_updated = replace(sample_game.round, cards_on_board=cards_on_board, tricks=tricks_before)
    sample_game_updated = replace(sample_game, round=round_updated)
    game = take_trick(sample_game_updated, taken_by=Seat(3))

    assert game.round.cards_to_take == []
    assert game.round.tricks == tricks_before + [cards_on_board]
    assert game.round.cards_on_board == {Seat(1): None, Seat(2): None, Seat(3): None}
    assert game.round.required_suit is None
    assert game.round.seat_infos[Seat(3)].points == 15  # 11 + 4 + 0
    assert game.active_seat == Seat(3)

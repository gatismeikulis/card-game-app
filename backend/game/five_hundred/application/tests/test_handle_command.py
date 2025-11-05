from dataclasses import replace
import pytest


from ....common.card import Rank, Suit
from ....common.hand import Hand
from ....common.game_exception import GameRulesException
from ...domain.five_hundred_deck import FiveHundredDeck
from ...domain.five_hundred_phase import FiveHundredPhase
from ...domain.five_hundred_command import (
    StartGameCommand,
    MakeBidCommand,
    PassCardsCommand,
    PlayCardCommand,
    GiveUpCommand,
)
from ...domain.five_hundred_event import (
    DeckShuffledEvent,
    BidMadeEvent,
    CardsPassedEvent,
    CardPlayedEvent,
    DeclarerGaveUpEvent,
)
from ...domain.five_hundred_card import FiveHundredCard
from ...domain.five_hundred_game import FiveHundredGame
from ..handle_command import handle_command


def test_handle_start_game_command(sample_game: FiveHundredGame):
    cmd = StartGameCommand()
    event = handle_command(game=sample_game, cmd=cmd)
    assert isinstance(event, DeckShuffledEvent)


def test_handle_make_bid_command_incorrect_phase(sample_game: FiveHundredGame):
    cmd = MakeBidCommand(bid=100)
    with pytest.raises(GameRulesException):
        _ = handle_command(sample_game, cmd)


@pytest.mark.parametrize(
    argnames="bid",
    argvalues=[20, 78, 1000, 95, 125],
    ids=[
        "too_low",
        "not_a_multiple_of_5",
        "too_high",
        "under_current_highest_bid",
        "too_high_for_hand_without_marriage",
    ],
)
def test_handle_make_bid_command_incorrect_bid_values(sample_game: FiveHundredGame, bid: int):
    round_updated = replace(sample_game.round, phase=FiveHundredPhase.BIDDING)
    game_updated = replace(sample_game, round=round_updated)
    cmd = MakeBidCommand(bid=bid)
    with pytest.raises(GameRulesException):
        _ = handle_command(game_updated, cmd)


def test_handle_make_bid_command_happy_path(sample_game: FiveHundredGame):
    round_updated = replace(sample_game.round, phase=FiveHundredPhase.BIDDING)
    game_updated = replace(sample_game, round=round_updated)
    cmd = MakeBidCommand(bid=round_updated.highest_bid[1] + 5 if round_updated.highest_bid else 105)
    event = handle_command(game_updated, cmd)
    assert event == BidMadeEvent(bid=cmd.bid, made_by=sample_game.active_seat)


def test_handle_give_up_command_incorrect_phase(sample_game: FiveHundredGame):
    cmd = GiveUpCommand()
    with pytest.raises(GameRulesException):
        _ = handle_command(sample_game, cmd)


def test_handle_give_up_command_happy_path(sample_game: FiveHundredGame):
    round_updated = replace(sample_game.round, phase=FiveHundredPhase.FORMING_HANDS)
    game_updated = replace(sample_game, round=round_updated)
    cmd = GiveUpCommand()
    event = handle_command(game_updated, cmd)
    assert event == DeclarerGaveUpEvent(made_by=sample_game.active_seat)


def test_handle_pass_cards_command_incorrect_phase(sample_game: FiveHundredGame):
    cmd = PassCardsCommand(
        card_to_next_seat=FiveHundredCard(Suit.CLUB, Rank.ACE), card_to_prev_seat=FiveHundredCard(Suit.CLUB, Rank.ACE)
    )
    with pytest.raises(GameRulesException):
        _ = handle_command(sample_game, cmd)


def test_handle_pass_cards_command_cards_not_in_hand(sample_game: FiveHundredGame):
    round_updated = replace(sample_game.round, phase=FiveHundredPhase.FORMING_HANDS)
    game_updated = replace(sample_game, round=round_updated)
    cmd = PassCardsCommand(
        card_to_next_seat=FiveHundredCard(Suit.CLUB, Rank.ACE), card_to_prev_seat=FiveHundredCard(Suit.CLUB, Rank.ACE)
    )
    with pytest.raises(GameRulesException):
        _ = handle_command(game_updated, cmd)


def test_handle_pass_cards_command_happy_path(sample_game: FiveHundredGame):
    deck = FiveHundredDeck.build()
    cards_to_add_to_hand = deck.draw_many(10)
    card_to_next_seat = cards_to_add_to_hand[0]
    card_to_prev_seat = cards_to_add_to_hand[1]

    active_seats_info_updated = replace(
        sample_game.active_seats_info, hand=Hand[FiveHundredCard](tuple(cards_to_add_to_hand))
    )
    seat_infos_updated = dict(sample_game.round.seat_infos) | {sample_game.active_seat: active_seats_info_updated}
    round_updated = replace(sample_game.round, seat_infos=seat_infos_updated, phase=FiveHundredPhase.FORMING_HANDS)
    game_updated = replace(sample_game, round=round_updated)
    cmd = PassCardsCommand(card_to_next_seat=card_to_next_seat, card_to_prev_seat=card_to_prev_seat)
    event = handle_command(game_updated, cmd)
    assert event == CardsPassedEvent(card_to_next_seat=cmd.card_to_next_seat, card_to_prev_seat=cmd.card_to_prev_seat)


def test_handle_play_card_command_incorrect_phase(sample_game: FiveHundredGame):
    cmd = PlayCardCommand(card=FiveHundredCard(Suit.CLUB, Rank.ACE))
    with pytest.raises(GameRulesException):
        _ = handle_command(sample_game, cmd)


def test_handle_play_card_command_card_not_in_hand(sample_game: FiveHundredGame):
    round_updated = replace(sample_game.round, phase=FiveHundredPhase.PLAYING_CARDS)
    game_updated = replace(sample_game, round=round_updated)
    cmd = PlayCardCommand(card=FiveHundredCard(Suit.CLUB, Rank.ACE))
    with pytest.raises(GameRulesException):
        _ = handle_command(game_updated, cmd)


def test_handle_play_card_command_happy_path(sample_game: FiveHundredGame):
    deck = FiveHundredDeck.build()
    cards_to_add_to_hand = deck.draw_many(10)
    card_to_play = cards_to_add_to_hand[0]

    active_seats_info_updated = replace(
        sample_game.active_seats_info, hand=Hand[FiveHundredCard](tuple(cards_to_add_to_hand))
    )
    seat_infos_updated = dict(sample_game.round.seat_infos) | {sample_game.active_seat: active_seats_info_updated}
    round_updated = replace(sample_game.round, seat_infos=seat_infos_updated, phase=FiveHundredPhase.PLAYING_CARDS)
    game_updated = replace(sample_game, round=round_updated)
    cmd = PlayCardCommand(card=card_to_play)
    event = handle_command(game_updated, cmd)
    assert event == CardPlayedEvent(card=card_to_play, played_by=sample_game.active_seat)

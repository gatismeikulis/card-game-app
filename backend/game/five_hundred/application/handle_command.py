from ...common.game_exception import GameRulesException
from ..domain.constants import (
    BID_STEP,
    CARDS_IN_STARTING_HAND,
    CARDS_TO_TAKE,
    MAX_BID,
    MIN_BID,
    NOT_ALLOWED_TO_BID_THRESHOLD,
)
from ..domain.five_hundred_deck import FiveHundredDeck
from ..domain.five_hundred_card import FiveHundredCard
from ..domain.five_hundred_command import (
    FiveHundredCommand,
    MakeBidCommand,
    PassCardsCommand,
    PlayCardCommand,
    StartGameCommand,
)
from ..domain.five_hundred_event import (
    BidMadeEvent,
    CardPlayedEvent,
    CardsPassedEvent,
    DeckShuffledEvent,
    FiveHundredEvent,
)
from ..domain.five_hundred_game import FiveHundredGame
from ..domain.five_hundred_phase import FiveHundredPhase


def handle_command(game: FiveHundredGame, cmd: FiveHundredCommand) -> FiveHundredEvent:
    match cmd:
        case StartGameCommand():
            return handle_start_game()
        case MakeBidCommand(bid=bid):
            return handle_make_bid(game, bid)
        case PassCardsCommand(card_to_next_seat=card_to_next_seat, card_to_prev_seat=card_to_prev_seat):
            return handle_pass_cards(game, card_to_next_seat, card_to_prev_seat)
        case PlayCardCommand(card=card):
            return handle_play_card(game, card)


def handle_start_game() -> FiveHundredEvent:
    deck = FiveHundredDeck.build()
    return DeckShuffledEvent(deck=deck)


def handle_make_bid(game: FiveHundredGame, bid: int) -> FiveHundredEvent:
    if game.round.phase != FiveHundredPhase.BIDDING:
        raise GameRulesException(message="Could not make bid: not 'bidding' phase")

    active_seats_match_points = game.summary[game.active_seat]
    if active_seats_match_points >= NOT_ALLOWED_TO_BID_THRESHOLD and bid >= 0:
        raise GameRulesException(message="Could not make bid: too many points to bid")
    if bid >= 0 and bid % BID_STEP != 0:
        raise GameRulesException(message=f"Could not make bid: bid must be with a step of {BID_STEP}")
    elif bid >= 0 and bid < MIN_BID:
        raise GameRulesException(message=f"Could not make bid: bid must be greater or equal to {MIN_BID}")
    elif bid > MAX_BID:
        raise GameRulesException(message=f"Could not make bid: bid is too high. Maximum bid is {MAX_BID}")
    elif bid >= 0 and game.round.highest_bid and bid <= game.round.highest_bid[1]:
        raise GameRulesException(
            message=f"Could not make bid: bid must be greater than current highest bid ({game.round.highest_bid[1]})"
        )

    return BidMadeEvent(bid=bid, made_by=game.active_seat)


def handle_pass_cards(
    game: FiveHundredGame,
    card_to_next_seat: FiveHundredCard,
    card_to_prev_seat: FiveHundredCard,
) -> FiveHundredEvent:
    if game.round.phase != FiveHundredPhase.FORMING_HANDS:
        raise GameRulesException(message="Could not pass cards: not 'forming hands' phase")

    active_seats_cards = game.active_seats_info.hand.cards

    if len(active_seats_cards) != CARDS_IN_STARTING_HAND + CARDS_TO_TAKE:
        raise GameRulesException(message="Could not pass cards: bidding winner has not taken hidden cards yet")

    if card_to_next_seat not in active_seats_cards or card_to_prev_seat not in active_seats_cards:
        raise GameRulesException(message="Could not pass cards: selected cards are not in the hand")

    return CardsPassedEvent(
        card_to_next_seat=card_to_next_seat,
        card_to_prev_seat=card_to_prev_seat,
    )


def handle_play_card(game: FiveHundredGame, card: FiveHundredCard) -> FiveHundredEvent:
    if game.round.phase != FiveHundredPhase.PLAYING_CARDS:
        raise GameRulesException(message="Could not play card: not 'playing cards' phase")

    active_seats_cards = game.active_seats_info.hand.cards

    if card not in active_seats_cards:
        raise GameRulesException(message="Could not play card: selected card is not in the hand")

    cards_allowed_to_play = game.active_seats_info.cards_allowed_to_play(
        game.round.required_suit, game.round.trump_suit
    )

    if card not in cards_allowed_to_play:
        raise GameRulesException(message="Could not play card: selected card is not allowed to play")

    return CardPlayedEvent(card=card, played_by=game.active_seat)

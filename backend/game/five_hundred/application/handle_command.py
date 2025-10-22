from ..domain.constants import BID_STEP, MAX_BID, MIN_BID
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
        raise ValueError("Cannot make bid. Not bidding phase.")

    active_seats_match_points = game.summary[game.active_seat]
    if active_seats_match_points >= 1000 and bid >= 0:
        raise ValueError(
            "Cannot make a bid. Player has reached more than 1000 points are not allowed to make non-passing bid."
        )

    if bid >= 0 and bid % BID_STEP != 0:
        raise ValueError(f"Invalid bid. Bid must be with a step of {BID_STEP}")
    elif bid >= 0 and bid < MIN_BID:
        raise ValueError(f"Bid must be greater or equal to {MIN_BID}")
    elif bid > MAX_BID:
        raise ValueError(f"Bid is too high. Maximum bid is {MAX_BID}")
    elif bid >= 0 and game.round.highest_bid and bid <= game.round.highest_bid[1]:
        raise ValueError(f"Bid must be greater than bid form previous bidder ({game.round.highest_bid[1]})")

    return BidMadeEvent(bid=bid, made_by=game.active_seat)


def handle_pass_cards(
    game: FiveHundredGame,
    card_to_next_seat: FiveHundredCard,
    card_to_prev_seat: FiveHundredCard,
) -> FiveHundredEvent:
    if game.round.phase != FiveHundredPhase.FORMING_HANDS:
        raise ValueError("Cannot pass cards. Not 'forming hands' phase.")

    active_seats_cards = game.active_seats_info.hand.cards

    if len(active_seats_cards) != 10:
        raise ValueError("Cannot pass cards. Bidding winner have not taken hidden cards yet.")

    if card_to_next_seat not in active_seats_cards or card_to_prev_seat not in active_seats_cards:
        raise ValueError("Cannot pass cards. Active seat do not have one or both of the passed cards.")

    return CardsPassedEvent(
        card_to_next_seat=card_to_next_seat,
        card_to_prev_seat=card_to_prev_seat,
    )


def handle_play_card(game: FiveHundredGame, card: FiveHundredCard) -> FiveHundredEvent:
    if game.round.phase != FiveHundredPhase.PLAYING_CARDS:
        raise ValueError("Cannot play card. Not 'playing cards' phase.")

    active_seats_cards = game.active_seats_info.hand.cards

    if card not in active_seats_cards:
        raise ValueError("Cannot play card. Active seat does not have the card.")

    cards_allowed_to_play = game.active_seats_info.cards_allowed_to_play(
        game.round.required_suit, game.round.trump_suit
    )

    if card not in cards_allowed_to_play:
        raise ValueError("Cannot play card. Card is not allowed to play.")

    return CardPlayedEvent(card=card, played_by=game.active_seat)

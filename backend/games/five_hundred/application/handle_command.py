from ..domain.constants import BID_STEP, MIN_BID, MAX_BID
from ..domain.five_hundred_card import FiveHundredCard
from ..domain.five_hundred_command import FiveHundredCommand, MakeBidCommand, PassCardsCommand, PlayCardCommand
from ..domain.five_hundred_event import (
    BidMadeEvent,
    CardPlayedEvent,
    CardsPassedEvent,
    FiveHundredEvent,
)
from ..domain.five_hundred_game import FiveHundredGame
from ..domain.five_hundred_phase import FiveHundredPhase


# if handler receives a command here, then it's already validated that command is received by active player.
# it should happen a layer above in table instance because table should have a dictionary of players and their seats
# and it can see if command sender is the same as active seat
# we only need to validate that actual command's data is valid for applying event
def handle_command(game: FiveHundredGame, cmd: FiveHundredCommand) -> FiveHundredEvent:
    match cmd:
        case MakeBidCommand(bid=bid):
            return handle_make_bid(game, bid)
        case PassCardsCommand(card_to_next_seat=card_to_next_seat, card_to_prev_seat=card_to_prev_seat):
            return handle_pass_cards(game, card_to_next_seat, card_to_prev_seat)
        case PlayCardCommand(card=card):
            return handle_play_card(game, card)


def handle_make_bid(game: FiveHundredGame, bid: int) -> FiveHundredEvent:
    if game.round.phase != FiveHundredPhase.BIDDING:
        raise ValueError("Cannot make bid. Not bidding phase.")

    active_seats_match_points = game.summary[game.round.active_seat]
    if active_seats_match_points >= 1000:
        raise ValueError("Cannot make bid. Player has reached more than 1000 points and is not allowed to bid.")

    if bid >= 0 and bid % BID_STEP != 0:
        raise ValueError(f"Invalid bid. Bid must be with a step of {BID_STEP}")
    elif bid >= 0 and bid < MIN_BID:
        raise ValueError(f"Bid must be greater or equal to {MIN_BID}")
    elif bid > MAX_BID:
        raise ValueError(f"Bid is too high. Maximum bid is {MAX_BID}")
    elif bid >= 0 and game.round.highest_bid and bid <= game.round.highest_bid[1]:
        raise ValueError(f"Bid must be greater than bid form previous bidder ({game.round.highest_bid[1]})")

    return BidMadeEvent(bid=bid, made_by=game.round.active_seat)


def handle_pass_cards(
    game: FiveHundredGame,
    card_to_next_seat: FiveHundredCard,
    card_to_prev_seat: FiveHundredCard,
) -> FiveHundredEvent:
    if game.round.phase != FiveHundredPhase.FORMING_HANDS:
        raise ValueError("Cannot pass cards. Not 'forming hands' phase.")

    active_seats_cards = game.round.active_seats_info.hand.cards

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

    active_seats_cards = game.round.active_seats_info.hand.cards

    if card not in active_seats_cards:
        raise ValueError("Cannot play card. Active seat does not have the card.")

    cards_allowed_to_play = game.round.active_seats_info.cards_allowed_to_play(
        game.round.required_suit, game.round.trump_suit
    )

    if card not in cards_allowed_to_play:
        raise ValueError("Cannot play card. Card is not allowed to play.")

    return CardPlayedEvent(card=card, played_by=game.round.active_seat)

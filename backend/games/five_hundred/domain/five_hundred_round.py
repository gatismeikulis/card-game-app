from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from ...common.card import Suit
from ...common.deck import Deck
from .constants import CARDS_IN_STARTING_HAND, CARDS_TO_TAKE
from .five_hundred_card import FiveHundredCard
from .five_hundred_phase import FiveHundredPhase
from .five_hundred_seat import FiveHundredSeat
from .five_hundred_seat_info import FiveHundredSeatInfo
from ...common.hand import Hand


@dataclass(frozen=True, slots=True)
class FiveHundredRound:
    _seat_infos: Mapping[FiveHundredSeat, FiveHundredSeatInfo]
    _cards_on_board: Mapping[FiveHundredSeat, FiveHundredCard | None]
    _cards_to_take: Sequence[FiveHundredCard]
    _required_suit: Suit | None
    _trump_suit: Suit | None
    _highest_bid: tuple[FiveHundredSeat, int] | None
    _phase: FiveHundredPhase
    _active_seat: FiveHundredSeat
    _round_number: int
    _first_seat: FiveHundredSeat  # seat which started this round
    _is_marriage_announced: bool

    @staticmethod
    def create(deck: Deck[FiveHundredCard], round_number: int, active_seat: FiveHundredSeat) -> "FiveHundredRound":
        cards_to_take = deck.draw_many(CARDS_TO_TAKE)
        seat_one_cards = deck.draw_many(CARDS_IN_STARTING_HAND)
        seat_two_cards = deck.draw_many(CARDS_IN_STARTING_HAND)
        seat_three_cards = deck.draw_many(CARDS_IN_STARTING_HAND)

        seat_infos: Mapping[FiveHundredSeat, FiveHundredSeatInfo] = {
            FiveHundredSeat(1): FiveHundredSeatInfo(
                _hand=Hand(seat_one_cards),
                _bid=0,
                _points=0,
                _trick_count=0,
                _marriage_points=[],
            ),
            FiveHundredSeat(2): FiveHundredSeatInfo(
                _hand=Hand(seat_two_cards),
                _bid=0,
                _points=0,
                _trick_count=0,
                _marriage_points=[],
            ),
            FiveHundredSeat(3): FiveHundredSeatInfo(
                _hand=Hand(seat_three_cards),
                _bid=0,
                _points=0,
                _trick_count=0,
                _marriage_points=[],
            ),
        }

        cards_on_board: Mapping[FiveHundredSeat, FiveHundredCard | None] = {
            FiveHundredSeat(1): None,
            FiveHundredSeat(2): None,
            FiveHundredSeat(3): None,
        }

        return FiveHundredRound(
            _seat_infos=seat_infos,
            _cards_on_board=cards_on_board,
            _cards_to_take=cards_to_take,
            _required_suit=None,
            _trump_suit=None,
            _highest_bid=None,
            _phase=FiveHundredPhase.BIDDING,
            _active_seat=active_seat,
            _round_number=round_number,
            _first_seat=active_seat,
            _is_marriage_announced=False,
        )

    @property
    def active_seats_info(self) -> FiveHundredSeatInfo:
        return self._seat_infos[self._active_seat]

    @property
    def seat_infos(self) -> Mapping[FiveHundredSeat, FiveHundredSeatInfo]:
        return self._seat_infos

    @property
    def cards_on_board(self) -> Mapping[FiveHundredSeat, FiveHundredCard | None]:
        return self._cards_on_board

    @property
    def cards_on_board_count(self) -> int:
        return sum(1 for v in self._cards_on_board.values() if v is not None)

    @property
    def cards_to_take(self) -> Sequence[FiveHundredCard]:
        return self._cards_to_take

    @property
    def required_suit(self) -> Suit | None:
        return self._required_suit

    @property
    def trump_suit(self) -> Suit | None:
        return self._trump_suit

    @property
    def highest_bid(self) -> tuple[FiveHundredSeat, int] | None:
        return self._highest_bid

    @property
    def phase(self) -> FiveHundredPhase:
        return self._phase

    @property
    def active_seat(self) -> FiveHundredSeat:
        return self._active_seat

    @property
    def round_number(self) -> int:
        return self._round_number

    @property
    def first_seat(self) -> FiveHundredSeat:
        return self._first_seat

    @property
    def is_marriage_announced(self) -> bool:
        return self._is_marriage_announced

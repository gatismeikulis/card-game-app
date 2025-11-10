import pytest
from ..game_exception import GameEngineException
from ..seat import Seat


def test_next_seat_valid():
    seat = Seat(1)
    next_seat = seat.next([Seat(2), Seat(3)])
    assert next_seat == Seat(2)


def test_prev_seat_valid():
    seat = Seat(1)
    prev_seat = seat.prev([Seat(2), Seat(3)])
    assert prev_seat == Seat(3)


def test_prev_seat_with_single_seat():
    seat = Seat(1)
    prev_seat = seat.prev([Seat(1)])
    assert prev_seat == Seat(1)  # Only one seat, wraps to itself


def test_next_seat_invalid():
    seat = Seat(1)
    with pytest.raises(GameEngineException):
        _ = seat.next([])


def test_from_dict_and_to_dict_roundtrip():
    seat = Seat(1)
    serialized = seat.to_dict()
    assert serialized == "1"
    deserialized = Seat.from_dict(int(serialized))
    assert deserialized == seat

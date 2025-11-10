from ..game_ending import GameEnding, GameEndingReason
from ..seat import Seat


def test_from_dict_and_to_dict_roundtrip():
    ending = GameEnding(
        winners=[Seat(1)],
        losers=[Seat(2)],
        reason=GameEndingReason.FINISHED,
        point_differences={Seat(1): 10, Seat(2): 20},
    )
    serialized = ending.to_dict()
    assert serialized == {
        "winners": ["1"],
        "losers": ["2"],
        "reason": "finished",
        "point_differences": {"1": 10, "2": 20},
    }
    deserialized = GameEnding.from_dict(serialized)
    assert deserialized == ending

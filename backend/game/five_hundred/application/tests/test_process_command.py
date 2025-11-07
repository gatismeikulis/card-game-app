from dataclasses import replace
import pytest_mock

from ...domain.five_hundred_game import FiveHundredGame
from ...domain.five_hundred_command import MakeBidCommand
from ...domain.five_hundred_event import (
    BidMadeEvent,
    BiddingFinishedEvent,
)
from .. import process_command as process_command_module


def test_process_command_runs_until_no_more_events(mocker: pytest_mock.MockerFixture, sample_game: FiveHundredGame):
    mock_handle = mocker.patch.object(process_command_module, "handle_command")
    mock_apply = mocker.patch.object(process_command_module, "apply_event")
    mock_check = mocker.patch.object(process_command_module, "check_for_additional_events")

    e1 = BidMadeEvent(bid=60, made_by=sample_game.active_seat)
    e2 = BiddingFinishedEvent(bid=60, made_by=sample_game.active_seat)

    mock_handle.return_value = e1
    mock_check.side_effect = [e2, None]
    mock_apply.return_value = sample_game

    game_updated, events = process_command_module.process_command(sample_game, MakeBidCommand(bid=60))

    assert game_updated == sample_game
    assert events == [e1, e2]
    mock_handle.assert_called_once()
    assert mock_apply.call_count == 2
    assert mock_check.call_count == 2


def test_check_for_additional_events_bidding_finished_if_all_passed(sample_game: FiveHundredGame):
    event = BidMadeEvent(bid=-1, made_by=sample_game.active_seat)

    # all seats passed
    seat_infos_updated = {seat: replace(seat_info, bid=-1) for seat, seat_info in sample_game.round.seat_infos.items()}
    round_updated = replace(sample_game.round, seat_infos=seat_infos_updated)
    game_updated = replace(sample_game, round=round_updated)

    result = process_command_module.check_for_additional_events(game_updated, event)
    assert isinstance(result, BiddingFinishedEvent)

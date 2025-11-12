from typing import Any
from django.db.models import QuerySet
import dramatiq
import logging

from .models import GameEventModel
from .registries.game_classes import get_game_class
from .registries.game_event_parsers import get_game_event_parser
from .domain.table_status import TableStatus
from .dependencies import (
    get_table_manager,
    get_task_lock_repository,
    get_game_event_repository,
    get_game_state_snapshot_repository,
)
from game.common.game_state import GameState

logger = logging.getLogger(__name__)


@dramatiq.actor()
def create_game_state_snapshots(
    table_id: str, start_event_number: int | None = None, end_event_number: int | None = None
) -> None:
    lock_key = f"create_game_state_snapshots_lock:{table_id}:{start_event_number}:{end_event_number}"

    lock_acquired = get_task_lock_repository().set_lock(lock_key)

    if not lock_acquired:
        logger.info(f"Game state snapshots creation for {table_id} already in progress, skipping...")
        return

    try:
        logger.info(f"Starting to create game state snapshots for table {table_id}")
        table = get_table_manager().get_table(table_id)

        if table.status == TableStatus.NOT_STARTED:
            logger.info(f"Game at table {table_id} is not started, skipping...")
            return

        db_events: QuerySet[GameEventModel] = get_game_event_repository().find_many(
            table_id, start_event_number, end_event_number
        )

        raw_initial_game_state: dict[str, Any] | None = None

        if start_event_number and start_event_number > 0:
            raw_initial_game_state = get_game_state_snapshot_repository().get(
                table_id, turn_number=None, event_number=start_event_number - 1
            )

        game_state: GameState | None = None

        if raw_initial_game_state:
            game_state = get_game_class(table.config.game_name).from_dict(raw_initial_game_state)

        data_to_store: list[dict[str, Any]] = []

        game_event_parser = get_game_event_parser(table.config.game_name)

        for db_event in db_events:
            event = game_event_parser.from_dict(db_event.data)
            state = table.get_game_state_after_event(game_state, event)

            turn_number = db_event.turn_number
            event_number = db_event.sequence_number

            data_to_store.append(
                {
                    "table_id": table_id,
                    "turn_number": turn_number,
                    "event_number": event_number,
                    "payload": state.to_dict(),
                }
            )

        get_game_state_snapshot_repository().store(data_to_store)
        logger.info(f"Game state snapshots for table {table_id} created and stored successfully!")
    except Exception as e:
        logger.error(f"Error: {e}")
    finally:
        get_task_lock_repository().release_lock(lock_key)

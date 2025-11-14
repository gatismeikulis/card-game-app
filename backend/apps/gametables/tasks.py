import dramatiq
import logging

from .dependencies import get_table_manager, get_task_lock_repository

logger = logging.getLogger(__name__)


@dramatiq.actor()
def create_all_game_state_snapshots_for_table(table_id: str) -> None:
    lock_key = f"create_all_game_state_snapshots_for_table:{table_id}"

    lock_acquired = get_task_lock_repository().set_lock(lock_key)

    if not lock_acquired:
        logger.info(f"Game state snapshots creation for {table_id} already in progress, skipping...")
        return

    try:
        logger.info(f"Starting to create all game state snapshots for table {table_id}")
        table_manager = get_table_manager()

        table = table_manager.get_table(table_id)

        if not table.is_game_ended:
            logger.info(f"Game at table {table_id} is not ended, skipping...")
            return

        _ = table_manager.create_and_store_game_state_snapshots(
            table=table, raw_initial_game_state=None, up_to_event_number=None
        )

        logger.info(f"Game state snapshots for table {table_id} created and stored successfully!")
    except Exception as e:
        logger.error(f"Error: {e}")
    finally:
        get_task_lock_repository().release_lock(lock_key)

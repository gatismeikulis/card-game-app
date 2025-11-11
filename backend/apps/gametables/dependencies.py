from redis import Redis

from .infra.task_lock_repository import TaskLockRepository
from .infra.game_state_snapshot_repository import GameStateSnapshotRepository
from .infra.game_table_repository import GameTableRepository
from .infra.game_event_repository import GameEventRepository
from .application.game_table_manager import GameTableManager
from config import settings

# Creating singletons at module load

redis_cache_conn = Redis.from_url(settings.REDIS_CACHE_URL)

game_table_repository = GameTableRepository()

game_event_repository = GameEventRepository()

game_state_snapshot_repository = GameStateSnapshotRepository(redis_conn=redis_cache_conn)

task_lock_repository = TaskLockRepository(redis_conn=redis_cache_conn)

table_manager = GameTableManager(
    game_table_repository=game_table_repository,
    game_event_repository=game_event_repository,
    game_state_snapshot_repository=game_state_snapshot_repository,
)

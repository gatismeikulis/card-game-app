from redis import Redis, ConnectionPool

from config import settings
from .infra.task_lock_repository import TaskLockRepository
from .infra.game_state_snapshot_repository import GameStateSnapshotRepository
from .infra.game_table_repository import GameTableRepository
from .infra.game_event_repository import GameEventRepository
from .application.game_table_manager import GameTableManager


# lazy, per-process singletons
_redis_cache_conn: Redis | None = None
_game_table_repo: GameTableRepository | None = None
_game_event_repo: GameEventRepository | None = None
_game_state_snapshot_repo: GameStateSnapshotRepository | None = None
_task_lock_repo: TaskLockRepository | None = None
_table_manager: GameTableManager | None = None


def get_redis_cache_conn() -> Redis:
    global _redis_cache_conn
    if _redis_cache_conn is None:
        pool = ConnectionPool.from_url(
            settings.REDIS_CACHE_URL,
            max_connections=50,
            retry_on_timeout=True,
            health_check_interval=30,
        )
        _redis_cache_conn = Redis(connection_pool=pool)
    return _redis_cache_conn


def get_game_table_repository() -> GameTableRepository:
    global _game_table_repo
    if _game_table_repo is None:
        _game_table_repo = GameTableRepository()
    return _game_table_repo


def get_game_event_repository() -> GameEventRepository:
    global _game_event_repo
    if _game_event_repo is None:
        _game_event_repo = GameEventRepository()
    return _game_event_repo


def get_game_state_snapshot_repository() -> GameStateSnapshotRepository:
    global _game_state_snapshot_repo
    if _game_state_snapshot_repo is None:
        _game_state_snapshot_repo = GameStateSnapshotRepository(redis_conn=get_redis_cache_conn())
    return _game_state_snapshot_repo


def get_task_lock_repository() -> TaskLockRepository:
    global _task_lock_repo
    if _task_lock_repo is None:
        _task_lock_repo = TaskLockRepository(redis_conn=get_redis_cache_conn())
    return _task_lock_repo


def get_table_manager() -> GameTableManager:
    global _table_manager
    if _table_manager is None:
        _table_manager = GameTableManager(
            game_table_repository=get_game_table_repository(),
            game_event_repository=get_game_event_repository(),
            game_state_snapshot_repository=get_game_state_snapshot_repository(),
        )
    return _table_manager

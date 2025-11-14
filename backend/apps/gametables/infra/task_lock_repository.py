from typing import override
from redis import Redis

from ..application.itask_lock_repository import ITaskLockRepository


class TaskLockRepository(ITaskLockRepository):
    def __init__(self, redis_conn: Redis):
        self.redis: Redis = redis_conn
        self.ttl_in_seconds: int = 60

    @override
    def set_lock(self, lock_key: str) -> bool:
        """
        Sets a lock for specific task if not already set.
        Returns True if lock was set, False if lock was already set, None if error occurred.
        """
        return bool(self.redis.set(lock_key, "1", nx=True, ex=self.ttl_in_seconds))

    @override
    def release_lock(self, lock_key: str) -> None:
        """
        Releases a lock for a specific task.
        """
        _ = self.redis.delete(lock_key)

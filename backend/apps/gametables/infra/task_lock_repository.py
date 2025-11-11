from redis import Redis


class TaskLockRepository:
    def __init__(self, redis_conn: Redis):
        self.redis: Redis = redis_conn
        self.ttl_in_seconds: int = 60

    def set_lock(self, lock_key: str) -> bool | None:
        """
        Sets a lock for specific task if not already set.
        Returns True if lock was set, False if lock was already set, None if error occurred.
        """
        return self.redis.set(lock_key, "1", nx=True, ex=self.ttl_in_seconds)

    def release_lock(self, lock_key: str) -> None:
        """
        Releases a lock for a specific task.
        """
        _ = self.redis.delete(lock_key)

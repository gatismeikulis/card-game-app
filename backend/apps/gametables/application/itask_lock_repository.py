from typing import Protocol


class ITaskLockRepository(Protocol):
    def set_lock(self, lock_key: str) -> bool:
        """
        Sets a lock for specific task to prevent .
        """
        ...

    def release_lock(self, lock_key: str) -> None:
        """
        Releases a lock for a specific table.
        """
        ...

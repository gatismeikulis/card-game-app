from typing import Protocol


class ITaskLockRepository(Protocol):
    def set_lock(self, table_id: str) -> None:
        """
        Sets a lock for specific task to prevent .
        """
        ...

    def release_lock(self, table_id: str) -> None:
        """
        Releases a lock for a specific table.
        """
        ...

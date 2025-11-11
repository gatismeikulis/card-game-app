from collections.abc import Sequence
from typing import Any, Protocol


class IGameStateSnapshotRepository(Protocol):
    def get(self, table_id: str, turn_number: int | None, event_number: int | None) -> dict[str, Any] | None:
        """
        Gets serialized game-state snapshot for specific table based on turn (priority) or event number (secondary).
        If none provided, returns initial game state snapshot.
        """
        ...

    def store(self, snapshots: Sequence[dict[str, Any]]) -> None:
        """
        Stores serialized game-state snapshots in bulk.
        """
        ...

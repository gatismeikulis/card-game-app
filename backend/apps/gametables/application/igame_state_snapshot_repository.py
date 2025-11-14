from collections.abc import Mapping, Sequence
from typing import Any, Protocol


class IGameStateSnapshotRepository(Protocol):
    def get_exact_or_nearest_snapshot_data(self, table_id: str, event_number: int = 0) -> Mapping[str, Any] | None:
        f"""
        Gets serialized game-state snapshot and metadata for specific table based on event number
        Returns: {"is_exact": bool, "snapshot": dict[str, Any]}
        """
        ...

    def store(self, table_id: str, raw_snapshots: Sequence[dict[str, Any]]) -> None:
        """
        Stores serialized game-state snapshots in bulk.
        """
        ...

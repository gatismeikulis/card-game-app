from collections.abc import Sequence
from typing import Protocol

from game.common.game_event import GameEvent


class IGameEventRepository(Protocol):
    def find_many(
        self, table_id: str, start_inclusive: int | None = None, end_inclusive: int | None = None
    ) -> Sequence[GameEvent]:
        """List/browse game events by table ID and sequence numbers (inclusive) sorted by sequence number ascending"""
        ...

from collections.abc import Sequence
from typing import Protocol, Any

from game.common.game_event import GameEvent


class IGamePlayEventRepository(Protocol):
    def append(self, table_id: str, game_events: Sequence[GameEvent]) -> None: ...

    def find_many(
        self, table_id: str, start_inclusive: int | None = None, end_inclusive: int | None = None
    ) -> Sequence[GameEvent]: ...

    """
    Returns:
        series of game-events limited by provided sequence numbers (inclusive) sorted by sequence number ascending
    """

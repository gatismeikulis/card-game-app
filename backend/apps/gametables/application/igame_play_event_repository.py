from collections.abc import Sequence
from typing import Protocol

from game.common.game_event import GameEvent


class IGamePlayEventRepository(Protocol):
    # Returns last sequence number of the appended events
    def append(self, table_id: str, game_events: Sequence[GameEvent]) -> int: ...

    # Returns series of game-events limited by provided sequence numbers (inclusive) sorted by sequence number ascending
    def find_many(
        self, table_id: str, start_inclusive: int | None = None, end_inclusive: int | None = None
    ) -> Sequence[GameEvent]: ...

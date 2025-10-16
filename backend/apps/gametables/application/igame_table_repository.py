from dataclasses import dataclass
from typing import Protocol

from ..models import GameTableSnapshot
from ..domain.game_table import GameTable


@dataclass(frozen=True)
class FindByIdResult:
    game_table: GameTable
    from_cache: bool


class IGameTableRepository(Protocol):
    def find_many(self) -> list[GameTableSnapshot]:
        """List/browse tables - SQL only.
        Returns:
            Important data (id, name, player_count, status, some important config, etc.) of GameTableSnapshot
        """
        ...

    def find_by_id(self, id: str) -> FindByIdResult:
        """Get full table for manipulation - Cache first, then SQL if not in Cache.
        Returns:
            GameTable with a flag indicating if it was found in Cache.
        """
        ...

    def create(self, game_table: GameTable) -> str:
        """Create a new table - write to Cache and SQL.
        Returns:
            Table ID.
        """
        ...

    def update(self, game_table: GameTable) -> str:
        """Update table - always update Cache, update SQL only if status changed.
        Returns:
            Table ID.
        """
        ...

    def delete(self, id: str) -> str:
        """Remove table from active use. Remove from Cache only for now.
        Not sure how to handle this in SQL for now...
        Returns:
            Table ID.
        """
        ...

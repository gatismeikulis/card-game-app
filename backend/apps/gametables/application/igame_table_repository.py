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

    def update_in_cache(self, game_table: GameTable) -> bool:
        """Update table in Cache only.
        Returns:
            True if update was successful, False otherwise.
        """
        ...

    def update_in_db(self, game_table: GameTable) -> None:
        """Update table in SQL only."""
        ...

    def delete_from_db(self, id: str) -> None:
        """Remove from SQL."""
        ...

    def delete_from_cache(self, id: str) -> None:
        """Remove from Cache."""
        ...

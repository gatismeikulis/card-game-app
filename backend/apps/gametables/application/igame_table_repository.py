from typing import Protocol

from ..models import GameTableSnapshot
from ..domain.game_table import GameTable


class IGameTableRepository(Protocol):
    def find_many(self) -> list[GameTableSnapshot]:
        """List/browse tables by important fields (configs, status, players, etc.)
        Returns:
            List of GameTableSnapshots
        """
        ...

    def find_by_id(self, id: str) -> GameTable:
        """Get full table instance for manipulation by ID.
        Returns:
            GameTable
        """
        ...

    def create(self, game_table: GameTable) -> str:
        """Create a new GameTableSnapshot and all related models
        Returns:
            Table ID.
        """
        ...

    def update(self, game_table: GameTable) -> None:
        """Update GameTableSnapshot and all related models"""
        ...

    def update_status_and_data_only(self, game_table: GameTable) -> None:
        """Update only data field of GameTableSnapshot without updating related models (configs, players, etc.)"""
        ...

    def delete(self, id: str) -> None:
        """Remove GameTableSnapshot and all related models"""
        ...

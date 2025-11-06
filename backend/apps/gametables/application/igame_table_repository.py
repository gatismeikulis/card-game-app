from collections.abc import Sequence
from typing import Callable, Protocol
from django.db.models import QuerySet

from ..domain.table_status import TableStatus
from game.common.game_event import GameEvent
from game.common.game_state import GameState
from ..models import GameTableModel
from ..domain.game_table import GameTable


class IGameTableRepository(Protocol):
    def find_many(self, filters: dict[str, set[str]]) -> QuerySet[GameTableModel]:
        """List/browse tables by important fields (configs, status, players, etc.)
        Returns:
            QuerySet of GameTableModel
        """
        ...

    def find_by_id(self, id: str) -> GameTable:
        """Get full GameTable instance by ID.
        Returns:
            GameTable instance
        """
        ...

    def create(self, game_table: GameTable) -> str:
        """Create a new GameTable instance, create new GameTableModel record and all related models
        Returns:
            Table ID.
        """
        ...

    def modify_during_game_action(
        self, table_id: str, modifier: Callable[[GameTable], Sequence[GameEvent]]
    ) -> tuple[Sequence[GameEvent], GameState, TableStatus]:
        """Modify GameTable instance according to passed modifier (only GameState is updated, table status only changes when game ends), update GameTableModel record and append emitted events
        Returns:
            Tuple of sequence of game events, updated GameState, table status
        """
        ...

    def modify(self, table_id: str, modifier: Callable[[GameTable], None]) -> GameTable:
        """Modify GameTable instance according to passed modifier, update GameTableModel record and related models without appending events
        Returns:
            The modified GameTable instance
        """
        ...

    def delete(self, id: str) -> None:
        """Remove GameTableModel record and all related models"""
        ...

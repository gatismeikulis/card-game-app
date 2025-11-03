from collections.abc import Sequence
from typing import Callable, Protocol
from django.db.models import QuerySet

from game.common.game_event import GameEvent
from ..models import GameTableSnapshot
from ..domain.game_table import GameTable


class IGameTableRepository(Protocol):
    def find_many(self, filters: dict[str, set[str]]) -> QuerySet[GameTableSnapshot]:
        """List/browse tables by important fields (configs, status, players, etc.)
        Returns:
            QuerySet of GameTableSnapshots
        """
        ...

    def find_by_id(self, id: str) -> GameTable:
        """Get full game table instance.
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

    def modify_during_game_action(
        self, table_id: str, modifier: Callable[[GameTable], Sequence[GameEvent]]
    ) -> tuple[Sequence[GameEvent], GameTable]:
        """Modify GameTableSnapshot and append emitted events
        Returns:
            Tuple of sequence of game events and the modified GameTable
        """
        ...

    def modify(self, table_id: str, modifier: Callable[[GameTable], None]) -> GameTable:
        """Modify GameTableSnapshot and related models without appending events
        Returns:
            The modified GameTable
        """
        ...

    def delete(self, id: str) -> None:
        """Remove GameTableSnapshot and all related models"""
        ...

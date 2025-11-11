from typing import Protocol
from django.db.models import QuerySet

from ..models import GameEventModel


class IGameEventRepository(Protocol):
    def find_many(
        self, table_id: str, start_inclusive: int | None = None, end_inclusive: int | None = None
    ) -> QuerySet[GameEventModel]:
        """List/browse game events by table ID and sequence numbers (inclusive) sorted by sequence number ascending
        Returns:
            QuerySet of GameEventModel
        """
        ...

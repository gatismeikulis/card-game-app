from collections.abc import Sequence

from backend.domain.table.game_table import GameTable
from backend.domain.table.game_table_config import GameTableConfig
from backend.domain.table.game_table_factory import GameTableFactory
from backend.domain.table.table_id import TableId


class Lobby:
    def __init__(self) -> None:
        self._tables: dict[TableId, GameTable] = {}

    def add_table(self, config: GameTableConfig) -> None:
        table = GameTableFactory.create(config)
        self._tables[table.id] = table

    def remove_table(self, table_id: TableId) -> None:
        del self._tables[table_id]

    def get_tables(self) -> Sequence[GameTable]:
        return tuple(self._tables.values())

    def table_by_id(self, table_id: TableId) -> GameTable:
        if table_id not in self._tables:
            raise ValueError(f"Table {table_id} not found in lobby")
        return self._tables[table_id]

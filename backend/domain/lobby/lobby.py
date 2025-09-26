from typing import Any

from backend.domain.game.game_name import GameName
from backend.domain.table.game_table import GameTable
from backend.domain.table.game_table_config import GameTableConfig
from backend.domain.table.game_table_factory import GameTableFactory
from backend.domain.table.table_id import TableId


class Lobby:
    def __init__(self) -> None:
        self._tables: dict[TableId, GameTable[Any, Any, Any]] = {}

    def add_table(self, game_name: GameName, config: GameTableConfig) -> None:
        table = GameTableFactory.create(config, game_name)
        self._tables[table.id] = table

    def remove_table(self, table_id: TableId) -> None:
        del self._tables[table_id]

    def get_tables(
        self,
    ) -> list[GameTable[Any, Any, Any]]:  # TODO Add some kind of filter here
        return list(self._tables.values())

    def table_by_id(self, table_id: TableId) -> GameTable[Any, Any, Any]:
        return self._tables[table_id]

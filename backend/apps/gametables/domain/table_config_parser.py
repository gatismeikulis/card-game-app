from typing import Any, Protocol

from .table_config import TableConfig


class TableConfigParser(Protocol):
    def from_dict(self, raw_config: dict[str, Any]) -> TableConfig: ...

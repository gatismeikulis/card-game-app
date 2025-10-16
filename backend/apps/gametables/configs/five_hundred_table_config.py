from dataclasses import dataclass
from typing import Any, override

from ..domain.table_config import TableConfig


@dataclass(frozen=True, slots=True)
class FiveHundredTableConfig(TableConfig):
    automatic_start: bool
    bots_allowed: bool

    @override
    def to_dict(self) -> dict[str, Any]:
        """Serialize to JSON-compatible dict"""
        return {"automatic_start": self.automatic_start, "bots_allowed": self.bots_allowed}


class FiveHundredTableConfigParser:
    def from_dict(self, raw_config: dict[str, Any]) -> TableConfig:
        # TODO validate
        automatic_start = raw_config.get("automatic_start", True)
        bots_allowed = raw_config.get("bots_allowed", True)
        return FiveHundredTableConfig(automatic_start=automatic_start, bots_allowed=bots_allowed)

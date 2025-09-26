from typing import Any

from backend.domain.game.five_hundred.domain.five_hundred_command import FiveHundredCommand
from backend.domain.game.five_hundred.domain.five_hundred_event import FiveHundredEvent
from backend.domain.game.five_hundred.domain.five_hundred_game import FiveHundredGame
from backend.domain.game.five_hundred.five_hundred_game_engine import FiveHundredGameEngine
from backend.domain.game.game_name import GameName
from backend.domain.table.game_table import GameTable
from backend.domain.table.game_table_config import GameTableConfig
from backend.domain.table.table_id import TableId


class GameTableFactory:
    @staticmethod
    def create(config: GameTableConfig, game_name: GameName) -> GameTable[Any, Any, Any]:
        match game_name:
            case GameName.FIVE_HUNDRED:
                return GameTable[FiveHundredGame, FiveHundredCommand, FiveHundredEvent](
                    TableId.generate(), config, FiveHundredGameEngine()
                )

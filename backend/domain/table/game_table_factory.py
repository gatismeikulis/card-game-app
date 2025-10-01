from backend.domain.game.five_hundred.five_hundred_game_engine import FiveHundredGameEngine
from backend.domain.game.game_name import GameName
from backend.domain.table.game_table import GameTable
from backend.domain.table.game_table_config import GameTableConfig
from backend.domain.table.table_id import TableId


class GameTableFactory:
    @staticmethod
    def create(config: GameTableConfig) -> GameTable:
        match config.game_name:
            case GameName.FIVE_HUNDRED:
                return GameTable(TableId.generate(), config, FiveHundredGameEngine())

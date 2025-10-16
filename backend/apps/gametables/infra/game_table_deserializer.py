from typing import Any

from ..registries.game_classes import get_game_class
from ..domain.table_status import TableStatus
from ..registries.table_config_parsers import get_table_config_parser
from ..registries.game_config_parsers import get_game_config_parser
from ..domain.game_table import GameTable
from ..domain.player import Player
from ..domain.game_table_config import GameTableConfig
from ..registries.game_engines import get_game_engine
from ..registries.bot_strategies import get_bot_strategy
from game.game_name import GameName
from game.bot_strategy_kind import BotStrategyKind


class GameTableDeserializer:
    @staticmethod
    def deserialize_player(data: dict[str, Any], game_name: GameName) -> Player:
        bot_strategy = None
        if data["bot_strategy_kind"]:
            kind = BotStrategyKind(data["bot_strategy_kind"])
            bot_strategy = get_bot_strategy(game_name, kind)

        return Player(
            player_id=data["player_id"],
            seat_number=data["seat_number"],
            screen_name=data["screen_name"],
            user_id=data["user_id"],
            bot_strategy=bot_strategy,
        )

    @staticmethod
    def deserialize_config(data: dict[str, Any]) -> GameTableConfig:
        game_config = get_game_config_parser(GameName(data["game_name"])).from_dict(data["game_config"])
        table_config = get_table_config_parser(GameName(data["game_name"])).from_dict(data["table_config"])
        return GameTableConfig(GameName(data["game_name"]), game_config, table_config)

    @staticmethod
    def deserialize_table(data: dict[str, Any]) -> GameTable:
        """Reconstruct from JSON-compatible dict"""
        config = GameTableDeserializer.deserialize_config(data["config"])

        engine = get_game_engine(config.game_name)

        table = GameTable(
            table_id=data["id"],
            config=config,
            engine=engine,
            owner_id=data["owner_id"],
            status=TableStatus(data["status"]),
        )

        if data["game_state"]:
            table._game_state = get_game_class(config.game_name).from_dict(data["game_state"])

        for pdata in data["players"]:
            player = GameTableDeserializer.deserialize_player(pdata, config.game_name)
            table._players.append(player)

        return table

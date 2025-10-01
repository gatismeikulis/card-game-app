from typing import final

from backend.domain.game.bot_strategy_kind import BotStrategyKind
from backend.domain.game.common.bot_strategy import BotStrategy
from backend.domain.game.five_hundred.five_hundred_random_bot_strategy import FiveHundredRandomBotStrategy
from backend.domain.game.game_name import GameName


@final
class BotStrategyRegistry:
    def __init__(self) -> None:
        self._strategies: dict[tuple[GameName, BotStrategyKind], BotStrategy] = {
            (GameName.FIVE_HUNDRED, BotStrategyKind.RANDOM): FiveHundredRandomBotStrategy(),
        }

    def get(self, game_name: GameName, bot_strategy_kind: BotStrategyKind) -> BotStrategy:
        key = (game_name, bot_strategy_kind)
        if key not in self._strategies:
            raise ValueError(f"Unknown bot strategy: {game_name}/{bot_strategy_kind}")
        return self._strategies[key]

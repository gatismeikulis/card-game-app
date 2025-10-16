from collections.abc import Mapping

from game.bot_strategy_kind import BotStrategyKind
from game.common.bot_strategy import BotStrategy
from game.five_hundred.five_hundred_random_bot_strategy import FiveHundredRandomBotStrategy
from game.game_name import GameName

BOT_STRATEGIES: Mapping[tuple[GameName, BotStrategyKind], BotStrategy] = {
    (GameName.FIVE_HUNDRED, BotStrategyKind.RANDOM): FiveHundredRandomBotStrategy(),
}


def get_bot_strategy(game_name: GameName, kind: BotStrategyKind) -> BotStrategy:
    return BOT_STRATEGIES[(game_name, kind)]

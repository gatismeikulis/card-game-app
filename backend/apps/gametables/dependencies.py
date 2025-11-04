from .infra.game_table_repository import GameTableRepository
from .infra.game_play_event_repository import GamePlayEventRepository
from .application.game_table_manager import GameTableManager


# Creating singletons at module load
game_table_repository = GameTableRepository()
game_play_event_repository = GamePlayEventRepository()
table_manager = GameTableManager(
    game_table_repository=game_table_repository, game_play_event_repository=game_play_event_repository
)

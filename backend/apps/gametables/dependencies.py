from .infra.game_table_repository import GameTableRepository
from .infra.game_event_repository import GameEventRepository
from .application.game_table_manager import GameTableManager


# Creating singletons at module load
game_table_repository = GameTableRepository()
game_event_repository = GameEventRepository()
table_manager = GameTableManager(
    game_table_repository=game_table_repository, game_event_repository=game_event_repository
)

import json
from django.test import TestCase

from .domain.table_status import TableStatus
from game.five_hundred.five_hundred_command_parser import FiveHundredCommandParser

from .configs.five_hundred_table_config import FiveHundredTableConfig
from game.game_name import GameName
from game.bot_strategy_kind import BotStrategyKind
from game.five_hundred.domain.five_hundred_game_config import FiveHundredGameConfig
from .domain.game_table import GameTable
from .domain.game_table_config import GameTableConfig
from .infra.game_table_deserializer import GameTableDeserializer
from .registries.game_engines import get_game_engine
from .registries.bot_strategies import get_bot_strategy


class TestGameTableSerialization(TestCase):
    """Test serialization/deserialization round-trip"""

    def test_round_trip_with_game_started(self):
        """Test serialization with active game state"""
        # Arrange - Create and start game
        config = GameTableConfig(
            game_name=GameName.FIVE_HUNDRED,
            game_config=FiveHundredGameConfig(max_seats=3, min_seats=3),
            table_config=FiveHundredTableConfig(automatic_start=True, bots_allowed=True),
        )
        engine = get_game_engine(GameName.FIVE_HUNDRED)
        original_table = GameTable(table_id="test-table-id", config=config, engine=engine, owner_id=1)

        original_table.add_player(user_id=1, screen_name="Alice", preferred_seat_number=1)
        original_table.add_player(user_id=2, screen_name="Bob", preferred_seat_number=2)
        original_table.add_player(
            screen_name="Charlie",
            preferred_seat_number=3,
            bot_strategy=get_bot_strategy(GameName.FIVE_HUNDRED, BotStrategyKind.RANDOM),
        )
        original_table.start_game()
        _ = original_table.take_regular_turn(
            user_id=1, command=FiveHundredCommandParser().from_dict({"type": "make_bid", "params": {"bid": 100}})
        )

        # Act - Serialize → JSON → Deserialize
        data = original_table.to_dict()
        json_str = json.dumps(data)
        restored_data = json.loads(json_str)
        restored_table = GameTableDeserializer.deserialize_table(restored_data)

        # Assert - Game state preserved
        self.assertEqual(restored_table.game_state, original_table.game_state)
        self.assertEqual(restored_table.status, TableStatus.IN_PROGRESS)
        self.assertEqual(restored_table.config, config)

        # Verify round-trip produces identical JSON
        restored_data_2 = restored_table.to_dict()
        json_str_2 = json.dumps(restored_data_2)

        self.assertEqual(json_str, json_str_2)

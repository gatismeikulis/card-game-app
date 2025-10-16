from typing import Any
from rest_framework.fields import CharField, ChoiceField, DictField, IntegerField, SerializerMethodField
from rest_framework.serializers import ModelSerializer, Serializer

from game.bot_strategy_kind import BotStrategyKind
from game.game_name import GameName
from .models import GameTablePlayer, GameTableSnapshot


class GameTablePlayerSerializer(ModelSerializer[GameTablePlayer]):
    class Meta:
        model = GameTablePlayer
        fields = ["user", "screen_name", "bot_strategy_kind"]


class GameTableWithRelationsSerializer(ModelSerializer[GameTableSnapshot]):
    game_table_players = GameTablePlayerSerializer(many=True, read_only=True)
    game_config = SerializerMethodField(read_only=True)
    table_config = SerializerMethodField(read_only=True)

    class Meta:
        model = GameTableSnapshot
        fields = [
            "id",
            "game_name",
            "status",
            "owner_id",
            "created_at",
            "updated_at",
            "game_table_players",
            "table_config",
            "game_config",
        ]

    def get_game_config(self, obj: GameTableSnapshot) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for row in obj.game_configs.all():
            result[row.config_key] = row.data
        return result

    def get_table_config(self, obj: GameTableSnapshot) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for row in obj.table_configs.all():
            result[row.config_key] = row.data
        return result


class CreateGameTableRequestSerializer(Serializer[dict[str, Any]]):
    game_name: ChoiceField = ChoiceField(choices=[g.value for g in GameName])
    table_config: DictField = DictField(required=False, default=dict)
    game_config: DictField = DictField(required=False, default=dict)


class JoinGameTableRequestSerializer(Serializer[dict[str, Any]]):
    preferred_seat: IntegerField = IntegerField(required=False, default=None)


class AddBotRequestSerializer(Serializer[dict[str, Any]]):
    bot_strategy_kind: ChoiceField = ChoiceField(choices=[b.value for b in BotStrategyKind])
    preferred_seat: IntegerField = IntegerField()


class RemoveBotRequestSerializer(Serializer[dict[str, Any]]):
    seat_number: IntegerField = IntegerField()


class TakeRegularTurnRequestSerializer(Serializer[dict[str, Any]]):
    type: CharField = CharField()
    params: DictField = DictField(required=False, default=dict)

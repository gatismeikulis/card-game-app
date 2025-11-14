from typing import Any, override
from rest_framework.fields import (
    CharField,
    ChoiceField,
    DictField,
    IntegerField,
    SerializerMethodField,
    MultipleChoiceField,
)
from rest_framework.serializers import ModelSerializer, Serializer

from game.bot_strategy_kind import BotStrategyKind
from game.game_name import GameName
from .models import PlayerModel, GameTableModel
from .domain.table_status import TableStatus


class GameTablePlayerSerializer(ModelSerializer[PlayerModel]):
    class Meta:
        model = PlayerModel
        fields = ["user", "screen_name", "bot_strategy_kind"]


class GameTableWithRelationsSerializer(ModelSerializer[GameTableModel]):
    players = GameTablePlayerSerializer(many=True, read_only=True)
    game_config = SerializerMethodField(read_only=True)
    table_config = SerializerMethodField(read_only=True)

    class Meta:
        model = GameTableModel
        fields = [
            "id",
            "game_name",
            "status",
            "owner_id",
            "created_at",
            "updated_at",
            "players",
            "table_config",
            "game_config",
        ]

    def get_game_config(self, obj: GameTableModel) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for row in obj.game_configs.all():
            result[row.config_key] = row.value
        return result

    def get_table_config(self, obj: GameTableModel) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for row in obj.table_configs.all():
            result[row.config_key] = row.value
        return result


class CreateGameTableRequestSerializer(Serializer[dict[str, Any]]):
    game_name: ChoiceField = ChoiceField(choices=[g.value for g in GameName])
    table_config: DictField = DictField(required=False, default=dict)
    game_config: DictField = DictField(required=False, default=dict)


class JoinGameTableRequestSerializer(Serializer[dict[str, Any]]):
    preferred_seat: IntegerField = IntegerField(required=False, default=None)


class AddBotRequestSerializer(Serializer[dict[str, Any]]):
    bot_strategy_kind: ChoiceField = ChoiceField(choices=[b.value for b in BotStrategyKind])
    preferred_seat: IntegerField = IntegerField(required=False, default=None)

    @override
    def to_internal_value(self, data: dict[str, Any]):
        if "bot_strategy_kind" in data:
            data_modified = data.copy()  # don't modify the original data passed to the serializer
            data_modified["bot_strategy_kind"] = data["bot_strategy_kind"].upper()
            return super().to_internal_value(data_modified)
        return super().to_internal_value(data)


class RemoveBotRequestSerializer(Serializer[dict[str, Any]]):
    seat_number: IntegerField = IntegerField()


class TakeRegularTurnRequestSerializer(Serializer[dict[str, Any]]):
    type: CharField = CharField()
    params: DictField = DictField(required=False, default=dict)


class CancelGameRequestSerializer(Serializer[dict[str, Any]]):
    type: CharField = CharField()
    params: DictField = DictField(required=False, default=dict)


class AbortGameRequestSerializer(Serializer[dict[str, Any]]):
    type: CharField = CharField()
    params: DictField = DictField(required=False, default=dict)
    to_blame: IntegerField = IntegerField()


class HistoryRequestQuerySerializer(Serializer[dict[str, int]]):
    event: IntegerField = IntegerField(required=True, min_value=0)


class CommaSeparatedMultipleChoiceField(MultipleChoiceField):
    """MultipleChoiceField that accepts comma-separated values"""

    def to_internal_value(self, data):
        if not data or data == [""]:
            return []
        split_data = [item.strip() for item in data[0].split(",")]
        return super().to_internal_value(split_data)


class TableListRequestQuerySerializer(Serializer[dict[str, Any]]):
    status = CommaSeparatedMultipleChoiceField(required=False, default=None, choices=[s.value for s in TableStatus])
    game_name = CommaSeparatedMultipleChoiceField(required=False, default=None, choices=[g.value for g in GameName])

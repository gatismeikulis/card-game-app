from django.db.models import (
    CASCADE,
    SET_NULL,
    ForeignKey,
    Index,
    Model,
    UUIDField,
    CharField,
    IntegerField,
    JSONField,
    DateTimeField,
)
from django.db.models.constraints import UniqueConstraint

from apps.users.models import User


class GameTableModel(Model):
    id = UUIDField(primary_key=True)
    game_name = CharField(max_length=50)
    status = CharField(max_length=30)
    owner = ForeignKey(User, on_delete=SET_NULL, null=True)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    snapshot = JSONField()  # serialized GameTable instance, snapshot

    class Meta:
        db_table = "gametable"
        indexes = [Index(fields=["game_name", "status"], name="game_name_status_index")]


class PlayerModel(Model):
    game_table = ForeignKey(GameTableModel, on_delete=CASCADE, related_name="players")
    user = ForeignKey(User, on_delete=SET_NULL, null=True)
    screen_name = CharField(max_length=50)
    bot_strategy_kind = CharField(max_length=50, null=True)

    class Meta:
        db_table = "gametable_player"
        constraints = [
            UniqueConstraint(fields=["game_table", "screen_name"], name="uniq_player_screen_name_per_table"),
            UniqueConstraint(fields=["game_table", "user"], name="uniq_player_user_per_table"),
        ]


class TableConfigModel(Model):
    game_table = ForeignKey(GameTableModel, on_delete=CASCADE, related_name="table_configs")
    config_key = CharField(max_length=100)
    value = JSONField()

    class Meta:
        db_table = "gametable_tableconfig"
        constraints = [
            UniqueConstraint(fields=["game_table", "config_key"], name="uniq_table_config_key_per_table"),
        ]


class GameConfigModel(Model):
    game_table = ForeignKey(GameTableModel, on_delete=CASCADE, related_name="game_configs")
    config_key = CharField(max_length=100)
    value = JSONField()

    class Meta:
        db_table = "gametable_gameconfig"
        constraints = [
            UniqueConstraint(fields=["game_table", "config_key"], name="uniq_game_config_key_per_table"),
        ]


class GameEventModel(Model):
    game_table = ForeignKey(GameTableModel, on_delete=CASCADE, related_name="game_events")
    sequence_number = IntegerField()
    data = JSONField()
    created_at = DateTimeField(auto_now_add=True)
    schema_version = IntegerField(default=1)

    class Meta:
        db_table = "gameevent"
        constraints = [
            UniqueConstraint(fields=["game_table", "sequence_number"], name="uniq_event_seq_per_table"),
        ]
        indexes = [Index(fields=["game_table", "sequence_number"], name="event_table_seq_idx")]
        ordering = ["sequence_number"]

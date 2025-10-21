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


class GameTableSnapshot(Model):
    id = UUIDField(primary_key=True)
    game_name = CharField(max_length=50)
    status = CharField(max_length=30)
    owner = ForeignKey(User, on_delete=SET_NULL, null=True)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    last_event_sequence_number = IntegerField(default=0)

    data = JSONField()  # serialized GameTable instance for easier game_table instance retrieval

    class Meta:
        indexes = [Index(fields=["game_name", "status"], name="game_name_status_index")]


class GameTablePlayer(Model):
    game_table = ForeignKey(GameTableSnapshot, on_delete=CASCADE, related_name="game_table_players")
    user = ForeignKey(User, on_delete=SET_NULL, null=True)
    screen_name = CharField(max_length=50)
    bot_strategy_kind = CharField(max_length=50, null=True)

    class Meta:
        constraints = [
            UniqueConstraint(fields=["game_table", "screen_name"], name="uniq_player_screen_name_per_table"),
            UniqueConstraint(fields=["game_table", "user"], name="uniq_player_user_per_table"),
        ]


class TableConfig(Model):
    game_table = ForeignKey(GameTableSnapshot, on_delete=CASCADE, related_name="table_configs")
    config_key = CharField(max_length=100)
    data = JSONField()

    class Meta:
        constraints = [
            UniqueConstraint(fields=["game_table", "config_key"], name="uniq_table_config_key_per_table"),
        ]


class GameConfig(Model):
    game_table = ForeignKey(GameTableSnapshot, on_delete=CASCADE, related_name="game_configs")
    config_key = CharField(max_length=100)
    data = JSONField()

    class Meta:
        constraints = [
            UniqueConstraint(fields=["game_table", "config_key"], name="uniq_game_config_key_per_table"),
        ]


class GamePlayEvent(Model):
    game_table = ForeignKey(GameTableSnapshot, on_delete=CASCADE, related_name="game_play_events")
    sequence_number = IntegerField()
    data = JSONField()
    created_at = DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            UniqueConstraint(fields=["game_table", "sequence_number"], name="uniq_event_seq_per_table"),
        ]

    # Consider adding (future improvements):
    # schema_version field to track schema changes in the future
    # user field to track the user who caused the event
    # index on game_table and sequence_number
    # index on game_table
    # ordering by sequence_number

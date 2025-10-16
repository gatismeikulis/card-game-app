from django.contrib import admin

from .models import GameTableSnapshot


class GameTableSnapshotAdmin(admin.ModelAdmin):
    fields = [
        "id",
        "owner",
        "game_name",
        "status",
        "created_at",
        "updated_at",
        "data",
        "game_configs",
        "table_configs",
        "game_play_events",
        "game_table_players",
    ]


admin.site.register(GameTableSnapshot, GameTableSnapshotAdmin)

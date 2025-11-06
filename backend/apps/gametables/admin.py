from django.contrib import admin

from .models import GameTableModel


class GameTableModelAdmin(admin.ModelAdmin):
    fields = [
        "id",
        "owner",
        "game_name",
        "status",
        "created_at",
        "updated_at",
        "snapshot",
        "game_configs",
        "table_configs",
        "events",
        "players",
    ]


admin.site.register(GameTableModel, GameTableModelAdmin)

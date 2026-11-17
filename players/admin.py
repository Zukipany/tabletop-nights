from django.contrib import admin

from players.models import Player


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('nickname', 'full_name', 'skill_level', 'favorite_game')
    list_filter = ('skill_level',)
    search_fields = ('nickname', 'full_name')

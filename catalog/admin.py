from django.contrib import admin

from catalog.models import BoardGame


@admin.register(BoardGame)
class BoardGameAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'min_players', 'max_players', 'playtime_minutes')
    list_filter = ('category',)
    search_fields = ('name',)

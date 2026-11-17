from django.contrib import admin

from nights.models import GameNight


@admin.register(GameNight)
class GameNightAdmin(admin.ModelAdmin):
    list_display = ('title', 'starts_at', 'location', 'host')
    list_filter = ('starts_at',)
    filter_horizontal = ('games', 'attendees')

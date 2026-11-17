from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from catalog.models import BoardGame
from nights.forms import GameNightCreateForm
from nights.models import GameNight
from players.models import Player


class GameNightTests(TestCase):
    def setUp(self):
        self.game = BoardGame.objects.create(name='Catan', min_players=3, max_players=4, playtime_minutes=90)
        self.host = Player.objects.create(nickname='host', full_name='Host Person')
        self.guest = Player.objects.create(nickname='guest', full_name='Guest Person')

    def form(self, **overrides):
        data = {'title': 'Friday', 'location': 'Home', 'max_seats': 4, 'host': self.host.pk,
                'games': [self.game.pk], 'attendees': [self.guest.pk],
                'starts_at': (timezone.now() + timedelta(days=2)).strftime('%Y-%m-%dT%H:%M')}
        data.update(overrides)
        return GameNightCreateForm(data=data)

    def test_valid_night(self):
        self.assertTrue(self.form().is_valid())

    def test_cannot_start_in_the_past(self):
        past = (timezone.now() - timedelta(days=1)).strftime('%Y-%m-%dT%H:%M')
        self.assertIn('starts_at', self.form(starts_at=past).errors)

    def test_host_cannot_be_attendee(self):
        self.assertIn('attendees', self.form(attendees=[self.host.pk]).errors)

    def test_players_must_fit_on_seats(self):
        self.assertIn('attendees', self.form(max_seats=2, attendees=[self.guest.pk, Player.objects.create(nickname='third', full_name='Third One').pk]).errors)

    def test_cannot_delete_player_who_hosts(self):
        night = GameNight.objects.create(title='Friday', location='Home', host=self.host,
                                         starts_at=timezone.now() + timedelta(days=1))
        night.games.add(self.game)
        self.client.post(reverse('player-delete', args=[self.host.pk]))
        self.assertTrue(Player.objects.filter(pk=self.host.pk).exists())

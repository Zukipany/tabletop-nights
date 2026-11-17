from django.test import TestCase
from django.urls import reverse

from catalog.forms import BoardGameCreateForm
from catalog.models import BoardGame


class BoardGameTests(TestCase):
    def valid_data(self, **overrides):
        data = {'name': 'Catan', 'category': 'strategy', 'min_players': 3,
                'max_players': 4, 'playtime_minutes': 90, 'complexity': 2}
        data.update(overrides)
        return data

    def test_max_players_cannot_be_less_than_min(self):
        form = BoardGameCreateForm(data=self.valid_data(min_players=5, max_players=3))
        self.assertFalse(form.is_valid())
        self.assertIn('max_players', form.errors)

    def test_create_redirects_to_detail(self):
        response = self.client.post(reverse('game-create'), self.valid_data())
        game = BoardGame.objects.get(name='Catan')
        self.assertRedirects(response, game.get_absolute_url())

    def test_player_range(self):
        game = BoardGame(min_players=2, max_players=4)
        self.assertEqual(game.player_range, '2–4 players')

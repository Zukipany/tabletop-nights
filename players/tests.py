from django.test import TestCase

from players.forms import PlayerCreateForm


class PlayerFormTests(TestCase):
    def test_nickname_rejects_spaces(self):
        form = PlayerCreateForm(data={'nickname': 'a b', 'full_name': 'Ana Ivanova', 'skill_level': 'casual'})
        self.assertIn('nickname', form.errors)

    def test_full_name_is_cleaned(self):
        form = PlayerCreateForm(data={'nickname': 'ana', 'full_name': '  ana   ivanova ', 'skill_level': 'casual'})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['full_name'], 'Ana Ivanova')

from django import forms
from django.utils import timezone

from common.forms import BootstrapFormMixin, ReadOnlyFieldsMixin
from nights.models import GameNight


class GameNightBaseForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = GameNight
        exclude = ['created_at']
        labels = {
            'starts_at': 'Date and time',
            'max_seats': 'Seats at the table',
            'games': 'Games to play',
            'attendees': 'Who is coming?',
        }
        help_texts = {
            'max_seats': 'Including the host.',
            'games': 'Hold Ctrl / Cmd to select several games.',
            'attendees': 'The host is counted automatically - do not select them here.',
        }
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'e.g. Friday Strategy Night'}),
            'starts_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'location': forms.TextInput(attrs={'placeholder': 'e.g. Ana\'s living room'}),
            'games': forms.SelectMultiple(attrs={'size': 5}),
            'attendees': forms.CheckboxSelectMultiple,
            'notes': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Bring snacks!'}),
        }
        error_messages = {
            'title': {'required': 'Give your game night a title.'},
            'starts_at': {'required': 'When does it start?', 'invalid': 'Please pick a valid date and time.'},
            'location': {'required': 'Where will you play?'},
            'host': {'required': 'Somebody has to host. Add a player first if the list is empty.'},
            'games': {'required': 'Pick at least one game. Add games to the shelf first if the list is empty.'},
        }

    def clean_starts_at(self):
        starts_at = self.cleaned_data['starts_at']
        if starts_at < timezone.now() and 'starts_at' in self.changed_data:
            raise forms.ValidationError('A new game night cannot start in the past.')
        return starts_at

    def clean(self):
        cleaned = super().clean()
        host = cleaned.get('host')
        attendees = cleaned.get('attendees')
        games = cleaned.get('games')
        max_seats = cleaned.get('max_seats')
        if host is None or attendees is None:
            return cleaned

        if host in attendees:
            self.add_error('attendees', f'{host} is the host and is already counted.')
            return cleaned

        total = len(attendees) + 1
        if max_seats and total > max_seats:
            self.add_error('attendees', f'{total} players do not fit on {max_seats} seats.')

        for game in games or []:
            if total > game.max_players:
                self.add_error('games', f'{game} supports at most {game.max_players} players, but {total} are coming.')
        return cleaned


class GameNightCreateForm(GameNightBaseForm):
    pass


class GameNightEditForm(ReadOnlyFieldsMixin, GameNightBaseForm):
    read_only_fields = ('host',)


class GameNightDeleteForm(ReadOnlyFieldsMixin, GameNightBaseForm):
    read_only_fields = '__all__'

    class Meta(GameNightBaseForm.Meta):
        fields = ['title', 'starts_at', 'location', 'host']
        exclude = None


class GameNightFilterForm(BootstrapFormMixin, forms.Form):
    WHEN_CHOICES = (('upcoming', 'Upcoming'), ('past', 'Past'), ('all', 'All'))

    q = forms.CharField(required=False, label='Search',
                        widget=forms.TextInput(attrs={'placeholder': 'Title or location...'}))
    when = forms.ChoiceField(required=False, choices=WHEN_CHOICES)

from django import forms

from catalog.models import BoardGame
from common.forms import BootstrapFormMixin, ReadOnlyFieldsMixin


class BoardGameBaseForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = BoardGame
        exclude = ['created_at']
        labels = {
            'name': 'Game name',
            'min_players': 'Min. players',
            'max_players': 'Max. players',
            'playtime_minutes': 'Play time (minutes)',
            'image_url': 'Box image URL',
        }
        help_texts = {
            'playtime_minutes': 'Average length of one game, between 5 and 600 minutes.',
            'complexity': 'How hard is it to learn?',
        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'e.g. Catan'}),
            'min_players': forms.NumberInput(attrs={'placeholder': '2'}),
            'max_players': forms.NumberInput(attrs={'placeholder': '4'}),
            'playtime_minutes': forms.NumberInput(attrs={'placeholder': '60'}),
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'What is the game about?'}),
            'image_url': forms.URLInput(attrs={'placeholder': 'https://...'}),
        }
        error_messages = {
            'name': {'required': 'Please give the game a name.'},
            'min_players': {'required': 'How many players are needed at least?'},
            'max_players': {'required': 'How many players can play at most?'},
            'playtime_minutes': {'required': 'Please enter the play time.'},
            'image_url': {'invalid': 'Please enter a valid web address starting with http(s)://'},
        }

    def clean_name(self):
        return self.cleaned_data['name'].strip()


class BoardGameCreateForm(BoardGameBaseForm):
    pass


class BoardGameEditForm(ReadOnlyFieldsMixin, BoardGameBaseForm):
    read_only_fields = ('name',)


class BoardGameDeleteForm(ReadOnlyFieldsMixin, BoardGameBaseForm):
    read_only_fields = '__all__'


class BoardGameFilterForm(BootstrapFormMixin, forms.Form):
    SORT_CHOICES = (
        ('name', 'Name (A–Z)'),
        ('-created_at', 'Newest first'),
        ('playtime_minutes', 'Shortest first'),
        ('-complexity', 'Most complex first'),
    )

    q = forms.CharField(required=False, label='Search',
                        widget=forms.TextInput(attrs={'placeholder': 'Search by name...'}))
    category = forms.ChoiceField(required=False, choices=[('', 'All categories'), *BoardGame.Category.choices])
    sort = forms.ChoiceField(required=False, choices=SORT_CHOICES)

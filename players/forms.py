from django import forms

from common.forms import BootstrapFormMixin, ReadOnlyFieldsMixin
from players.models import Player


class PlayerBaseForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Player
        exclude = ['joined_on']
        labels = {
            'full_name': 'Full name',
            'skill_level': 'Experience',
            'favorite_game': 'Favourite game',
            'bio': 'About',
        }
        help_texts = {
            'nickname': 'Letters, digits and underscores only. Shown everywhere on the site.',
            'favorite_game': 'Optional. Pick one from the game shelf.',
        }
        widgets = {
            'nickname': forms.TextInput(attrs={'placeholder': 'e.g. dice_queen'}),
            'full_name': forms.TextInput(attrs={'placeholder': 'e.g. Ana Ivanova'}),
            'bio': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Favourite genres, house rules...'}),
        }
        error_messages = {
            'nickname': {'required': 'Every player needs a nickname.'},
            'full_name': {'required': 'Please enter the player\'s name.'},
        }

    def clean_full_name(self):
        full_name = ' '.join(self.cleaned_data['full_name'].split())
        if any(char.isdigit() for char in full_name):
            raise forms.ValidationError('A name cannot contain digits.')
        return full_name.title()


class PlayerCreateForm(PlayerBaseForm):
    pass


class PlayerEditForm(ReadOnlyFieldsMixin, PlayerBaseForm):
    read_only_fields = ('nickname',)


class PlayerDeleteForm(ReadOnlyFieldsMixin, PlayerBaseForm):
    read_only_fields = '__all__'


class PlayerFilterForm(BootstrapFormMixin, forms.Form):
    q = forms.CharField(required=False, label='Search',
                        widget=forms.TextInput(attrs={'placeholder': 'Nickname or name...'}))
    level = forms.ChoiceField(required=False, choices=[('', 'All levels'), *Player.SkillLevel.choices])

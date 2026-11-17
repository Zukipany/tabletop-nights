from django.core.validators import MinLengthValidator, RegexValidator
from django.db import models
from django.urls import reverse


class Player(models.Model):
    """A person who joins game nights (not a site user - there is no login)."""

    class SkillLevel(models.TextChoices):
        BEGINNER = 'beginner', 'Beginner'
        CASUAL = 'casual', 'Casual'
        VETERAN = 'veteran', 'Veteran'

    nickname = models.CharField(
        max_length=30,
        unique=True,
        validators=[
            MinLengthValidator(3, 'The nickname must be at least 3 characters long.'),
            RegexValidator(r'^[A-Za-z0-9_]+$', 'Use only letters, digits and underscores.'),
        ],
        error_messages={'unique': 'This nickname is already taken.'},
    )
    full_name = models.CharField(max_length=80)
    skill_level = models.CharField(max_length=10, choices=SkillLevel.choices, default=SkillLevel.CASUAL)
    favorite_game = models.ForeignKey(
        'catalog.BoardGame',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='fans',
    )
    bio = models.TextField(blank=True)
    joined_on = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['nickname']

    def __str__(self):
        return self.nickname

    def get_absolute_url(self):
        return reverse('player-detail', kwargs={'pk': self.pk})

    @property
    def initials(self):
        return ''.join(part[0] for part in self.full_name.split()[:2]).upper()

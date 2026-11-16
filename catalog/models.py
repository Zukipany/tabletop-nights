from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinLengthValidator, MinValueValidator
from django.db import models
from django.db.models import F, Q
from django.urls import reverse


class BoardGame(models.Model):
    class Category(models.TextChoices):
        STRATEGY = 'strategy', 'Strategy'
        PARTY = 'party', 'Party'
        COOPERATIVE = 'coop', 'Cooperative'
        FAMILY = 'family', 'Family'
        CARD = 'card', 'Card game'
        ABSTRACT = 'abstract', 'Abstract'

    class Complexity(models.IntegerChoices):
        VERY_LIGHT = 1, 'Very light'
        LIGHT = 2, 'Light'
        MEDIUM = 3, 'Medium'
        HEAVY = 4, 'Heavy'
        VERY_HEAVY = 5, 'Very heavy'

    name = models.CharField(
        max_length=100,
        unique=True,
        validators=[MinLengthValidator(2, 'The name must be at least 2 characters long.')],
        error_messages={'unique': 'A game with this name is already on the shelf.'},
    )
    category = models.CharField(max_length=20, choices=Category.choices, default=Category.STRATEGY)
    min_players = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(20)],
    )
    max_players = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(20)],
    )
    playtime_minutes = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(5, 'A game takes at least 5 minutes.'),
            MaxValueValidator(600, 'Games longer than 10 hours are not supported.'),
        ],
    )
    complexity = models.PositiveSmallIntegerField(choices=Complexity.choices, default=Complexity.MEDIUM)
    description = models.TextField(blank=True)
    image_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        constraints = [
            models.CheckConstraint(
                condition=Q(max_players__gte=F('min_players')),
                name='max_players_gte_min_players',
            ),
        ]

    def __str__(self):
        return self.name

    def clean(self):
        super().clean()
        if self.min_players and self.max_players and self.min_players > self.max_players:
            raise ValidationError({'max_players': 'Maximum players cannot be less than minimum players.'})

    def get_absolute_url(self):
        return reverse('game-detail', kwargs={'pk': self.pk})

    @property
    def player_range(self):
        if self.min_players == self.max_players:
            return f'{self.min_players} players'
        return f'{self.min_players}–{self.max_players} players'

    def supports(self, player_count):
        return self.min_players <= player_count <= self.max_players

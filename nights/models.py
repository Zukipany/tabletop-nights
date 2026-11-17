from django.core.validators import MaxValueValidator, MinLengthValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone


class GameNightQuerySet(models.QuerySet):
    def upcoming(self):
        return self.filter(starts_at__gte=timezone.now()).order_by('starts_at')

    def past(self):
        return self.filter(starts_at__lt=timezone.now()).order_by('-starts_at')


class GameNight(models.Model):
    title = models.CharField(
        max_length=80,
        validators=[MinLengthValidator(3, 'The title must be at least 3 characters long.')],
    )
    starts_at = models.DateTimeField()
    location = models.CharField(max_length=120)
    max_seats = models.PositiveSmallIntegerField(
        default=4,
        validators=[
            MinValueValidator(2, 'A game night needs at least 2 seats.'),
            MaxValueValidator(30, 'That is a party, not a game night (max 30 seats).'),
        ],
    )
    host = models.ForeignKey(
        'players.Player',
        on_delete=models.PROTECT,
        related_name='hosted_nights',
    )
    games = models.ManyToManyField('catalog.BoardGame', related_name='game_nights')
    attendees = models.ManyToManyField('players.Player', related_name='attended_nights', blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = GameNightQuerySet.as_manager()

    class Meta:
        ordering = ['-starts_at']

    def __str__(self):
        return f'{self.title} ({self.starts_at:%d %b %Y})'

    def get_absolute_url(self):
        return reverse('night-detail', kwargs={'pk': self.pk})

    @property
    def is_upcoming(self):
        return self.starts_at >= timezone.now()

    @property
    def total_players(self):
        """The host plus everyone who joined."""
        return self.attendees.count() + 1

    @property
    def seats_left(self):
        return max(self.max_seats - self.total_players, 0)

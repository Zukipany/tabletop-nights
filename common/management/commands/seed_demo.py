"""Optional MOCK demo data. The app works without it - run only if you want a filled-in example."""
from datetime import timedelta

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone

from catalog.models import BoardGame
from nights.models import GameNight
from players.models import Player

GAMES = [
    # name, category, min, max, minutes, complexity, description
    ('Catan', 'strategy', 3, 4, 90, 2, 'Trade wood, brick and sheep to build roads and cities on an island.'),
    ('Ticket to Ride', 'family', 2, 5, 60, 2, 'Collect coloured train cards and claim railway routes across the map.'),
    ('Codenames', 'party', 2, 8, 15, 1, 'Two teams guess secret words from one-word clues.'),
    ('Pandemic', 'coop', 2, 4, 45, 2, 'Work together to stop four diseases spreading around the world.'),
    ('Azul', 'abstract', 2, 4, 40, 2, 'Draft coloured tiles to decorate a palace wall.'),
    ('7 Wonders', 'strategy', 3, 7, 30, 2, 'Draft cards over three ages to build an ancient civilisation.'),
    ('Carcassonne', 'family', 2, 5, 35, 2, 'Place tiles to build a medieval landscape of cities, roads and fields.'),
    ('Wingspan', 'strategy', 1, 5, 70, 2, 'Attract birds to your wildlife preserves.'),
    ('Splendor', 'card', 2, 4, 30, 1, 'Collect gems to buy cards and attract nobles.'),
    ('Terraforming Mars', 'strategy', 1, 5, 120, 3, 'Compete to make Mars habitable.'),
    ('Dixit', 'party', 3, 8, 30, 1, 'Tell stories about dreamlike pictures and guess the right card.'),
    ('Gloomhaven', 'coop', 1, 4, 120, 4, 'A campaign of tactical dungeon fights with lasting consequences.'),
]

PLAYERS = [
    # nickname, full name, skill level, favourite game index
    ('dice_queen', 'Ana Ivanova', 'veteran', 0),
    ('meeple_max', 'Maxim Petrov', 'casual', 6),
    ('rook_rider', 'Elena Georgieva', 'veteran', 9),
    ('pawn_star', 'Ivan Dimitrov', 'beginner', 2),
    ('card_shark', 'Maria Koleva', 'casual', 8),
    ('tile_tom', 'Tom Nikolov', 'casual', 4),
    ('co_op_kate', 'Kate Stoyanova', 'veteran', 3),
    ('lucky_lazar', 'Lazar Todorov', 'beginner', 10),
]

NIGHTS = [
    'Friday Strategy Night', 'Rainy Sunday Games', 'Co-op Rescue Mission', 'Party Games Marathon',
    'Beginners Welcome', 'Train Tycoons', 'Quick Games After Work', 'Big Box Saturday',
    'Card Game Café', 'Tile Layers Club', 'Board Game Birthday', 'Mars Colony Evening',
    'Lunch Break Duel', 'Weekend Campaign Session', 'End of Month Game Night',
]

LOCATIONS = ["Ana's living room", 'Board game café "The Meeple"', "Maxim's flat", 'Office kitchen', 'Student dorm, room 214']


class Command(BaseCommand):
    help = 'Loads MOCK demo data: 12 board games, 8 players and 15 game nights (past and upcoming).'

    def add_arguments(self, parser):
        parser.add_argument('--clear', action='store_true',
                            help='Delete ALL existing games, players and game nights before loading the demo data.')

    @transaction.atomic
    def handle(self, *args, **options):
        if options['clear']:
            GameNight.objects.all().delete()
            Player.objects.all().delete()
            BoardGame.objects.all().delete()
        elif BoardGame.objects.filter(name__in=[g[0] for g in GAMES]).exists():
            raise CommandError('Demo data seems to be loaded already. Run with --clear to reload it.')

        games = [
            BoardGame.objects.create(name=n, category=c, min_players=lo, max_players=hi,
                                     playtime_minutes=t, complexity=x, description=d)
            for n, c, lo, hi, t, x, d in GAMES
        ]
        players = [
            Player.objects.create(nickname=nick, full_name=name, skill_level=level, favorite_game=games[fav],
                                  bio='Mock demo player.')
            for nick, name, level, fav in PLAYERS
        ]

        today_7pm = timezone.localtime().replace(hour=19, minute=0, second=0, microsecond=0)
        for i, title in enumerate(NIGHTS):
            host = players[i % len(players)]
            guests = [p for p in players if p != host][i % 5:(i % 5) + 1 + i % 3]
            total = len(guests) + 1
            fitting = [g for g in games if g.supports(total)]
            night = GameNight.objects.create(
                title=title,
                starts_at=today_7pm + timedelta(days=(i - 7) * 3),  # 7 past nights, 8 upcoming
                location=LOCATIONS[i % len(LOCATIONS)],
                max_seats=max(total, 4),
                host=host,
                notes='Mock demo game night.',
            )
            night.games.set({fitting[(i * 5) % len(fitting)], fitting[(i * 5 + 4) % len(fitting)]})
            night.attendees.set(guests)

        self.stdout.write(self.style.SUCCESS(
            f'Loaded mock demo data: {len(games)} games, {len(players)} players, {len(NIGHTS)} game nights.'))

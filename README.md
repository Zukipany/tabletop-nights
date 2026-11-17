# 🎲 TableTop Nights

**TableTop Nights** is a Django web application for a group of friends who meet to play board games.
It answers three everyday questions of every board game group:

1. **What can we play?** - a shared *game shelf* with player counts, play time and complexity.
2. **Who is in the group?** - *player* profiles with experience level and favourite game.
3. **When and where do we meet, and what do we play?** - *game nights* with a host, attendees,
   selected games and a seat counter that shows how many places are left.

There is no login or registration. Everything is created, edited and deleted directly from the UI,
starting from an **empty database**.

---

## Table of contents

- [Quick start](#quick-start)
- [Environment variables](#environment-variables)
- [Mock demo data (optional)](#mock-demo-data-optional)
- [Walkthrough for the evaluator](#walkthrough-for-the-evaluator)
- [Features](#features)
- [Pages and URLs](#pages-and-urls)
- [Database design](#database-design)
- [Forms](#forms)
- [Validation rules and messages](#validation-rules-and-messages)
- [Views](#views)
- [Templates, filters and tags](#templates-filters-and-tags)
- [Tests](#tests)
- [Project structure](#project-structure)
- [OOP and code quality](#oop-and-code-quality)
- [AI usage](#ai-usage)

---

## Quick start

Requirements: **Python 3.12+**. Everything else is installed from `requirements.txt` (only Django).

```bash
git clone https://github.com/Zukipany/tabletop-nights.git
cd tabletop-nights
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Open **http://127.0.0.1:8000/**. The database starts empty and the app is fully usable that way.

## Environment variables

**None are required.** The project runs with safe local defaults. All variables are optional:

| Variable | Default | What it does |
|---|---|---|
| `DJANGO_SECRET_KEY` | an insecure local development key | Django secret key. Set your own outside local testing. |
| `DJANGO_DEBUG` | `False` | `True` shows Django's debug pages. With `False` the **custom 404 page** is shown. |
| `DJANGO_ALLOWED_HOSTS` | `localhost,127.0.0.1,testserver` | Comma separated list of allowed host names. |

No database credentials, API keys or other secrets are needed. The database is a local SQLite file
(`db.sqlite3`) created by `migrate`.

Example with debug mode on:

```bash
DJANGO_DEBUG=True python manage.py runserver
```

## Mock demo data (optional)

> ⚠️ **This is MOCK data for demonstration only.** All games descriptions, people, nicknames, places
> and events are made up. The application does **not** depend on it: it works with an empty database
> and every object can be created through the UI. The data is **not** loaded by migrations or fixtures -
> it is only added when you run the command below yourself.

If you want to see the app filled with content instead of starting from scratch, run:

```bash
python manage.py seed_demo
```

It creates:

| What | Amount | Details |
|---|---|---|
| Board games | 12 | Catan, Ticket to Ride, Codenames, Pandemic, Azul, 7 Wonders, Carcassonne, Wingspan, Splendor, Terraforming Mars, Dixit, Gloomhaven - different categories, player counts and complexity |
| Players | 8 | e.g. `dice_queen`, `meeple_max`, `card_shark`, each with a skill level and a favourite game |
| Game nights | 15 | 7 in the past and 8 upcoming (every 3 days around today), each with a host, 1-3 attendees and 2 different games that fit the number of players |

Every mock player has the bio *"Mock demo player."* and every mock game night has the note
*"Mock demo game night."*, so mock records are easy to recognise in the UI.

Useful options:

```bash
python manage.py seed_demo --clear   # deletes ALL games, players and nights, then loads the mock data again
python manage.py help seed_demo      # shows the help text
```

Running `seed_demo` twice without `--clear` stops with a friendly error instead of creating duplicates.

## Walkthrough for the evaluator

Starting from an empty database, this order creates one object of every model through the UI:

1. **Add game** (navbar) → e.g. *Catan*, 3-4 players, 90 minutes.
   Try min 5 / max 3 players to see the validation message.
2. **Add player** (navbar) → add two or three players.
   Try the nickname `a b` to see the validation message.
3. **Plan a night** (navbar button) → choose a host, at least one game and some attendees.
   Try a date in the past, or tick the host as an attendee, to see the validation messages.
4. **Home** → statistics, upcoming nights, newest and most played games are now filled in.
5. **Edit** any object → the identity field (game name / player nickname / night host) is read-only.
6. **Delete** any object → a confirmation page shows the object in a disabled form first.
   Deleting a player who hosts a game night is blocked with a message.
7. Open any unknown URL, e.g. `/does-not-exist/` → custom **404** page.

## Features

### Game shelf (`catalog` app)
- Add, view, edit and delete board games.
- List page with **search by name**, **filter by category**, **sorting** (name, newest, shortest, most complex)
  and **pagination** (6 per page). Search, filter and sort are kept when changing pages.
- Detail page with player range, play time (e.g. `1h 30m`), complexity as stars (`★★☆☆☆`), the players who
  chose it as favourite and how many game nights it is planned for.
- "Plan a night" button on a game pre-selects that game in the new night form.

### Players (`players` app)
- Add, view, edit and delete players.
- List page with **search by nickname or name** and **filter by skill level**.
- Detail page with bio, favourite game, the nights the player **hosts** and the nights they **join**.
- Names are tidied automatically (`  ana   ivanova ` → `Ana Ivanova`).

### Game nights (`nights` app)
- Plan, view, edit and cancel (delete) game nights.
- List page shows **upcoming** nights by default, with options for **past** and **all**, plus search
  by title or location.
- Detail page with date, location, host, attendees, games, notes and a **seat progress bar**
  (e.g. 3 / 4 seats taken, 1 seat left).
- Smart validation: no nights in the past, the host is counted automatically, everyone must fit on the
  seats and every chosen game must support that many players.

### Home page (`common` app)
- Live statistics (games, players, game nights).
- The next three upcoming game nights.
- Newest games on the shelf and a "most played" ranking.

### Everywhere
- Bootstrap 5 layout, responsive navbar and footer on every page.
- Success and error messages after every create, edit and delete.
- Custom 404 page ("You rolled a one!").

## Pages and URLs

| Page | URL | Shows database data |
|---|---|---|
| Home / dashboard | `/` | ✅ |
| Game list (search, filter, sort) | `/games/` | ✅ |
| Game details | `/games/<id>/` | ✅ |
| Add game | `/games/add/` | |
| Edit game | `/games/<id>/edit/` | ✅ |
| Delete game (confirmation) | `/games/<id>/delete/` | ✅ |
| Player list (search, filter) | `/players/` | ✅ |
| Player details | `/players/<id>/` | ✅ |
| Add player | `/players/add/` | ✅ (favourite game choices) |
| Edit player | `/players/<id>/edit/` | ✅ |
| Delete player (confirmation) | `/players/<id>/delete/` | ✅ |
| Game night list (upcoming / past / all) | `/nights/` | ✅ |
| Game night details | `/nights/<id>/` | ✅ |
| Plan a game night | `/nights/add/` | ✅ (host, games, attendees choices) |
| Edit game night | `/nights/<id>/edit/` | ✅ |
| Cancel game night (confirmation) | `/nights/<id>/delete/` | ✅ |
| Custom 404 | any unknown URL | |

Every page is reachable from the navbar, the footer or a button on another page.

## Database design

```
BoardGame 1 ───< Player.favorite_game          (many-to-one, SET_NULL)
Player    1 ───< GameNight.host                (many-to-one, PROTECT)
GameNight >───< BoardGame   via GameNight.games      (many-to-many)
GameNight >───< Player      via GameNight.attendees  (many-to-many)
```

### `BoardGame` (`catalog`)
| Field | Type | Notes |
|---|---|---|
| `name` | CharField | unique, at least 2 characters |
| `category` | CharField + `TextChoices` | Strategy, Party, Cooperative, Family, Card game, Abstract |
| `min_players`, `max_players` | PositiveSmallIntegerField | 1-20, database `CheckConstraint` max ≥ min |
| `playtime_minutes` | PositiveSmallIntegerField | 5-600 |
| `complexity` | PositiveSmallIntegerField + `IntegerChoices` | 1 (very light) - 5 (very heavy) |
| `description`, `image_url` | TextField, URLField | optional |
| `created_at` | DateTimeField | set automatically |

Methods: `clean()`, `get_absolute_url()`, `player_range` property, `supports(player_count)`.

### `Player` (`players`)
| Field | Type | Notes |
|---|---|---|
| `nickname` | CharField | unique, 3+ characters, letters / digits / underscores only |
| `full_name` | CharField | |
| `skill_level` | CharField + `TextChoices` | Beginner, Casual, Veteran |
| `favorite_game` | ForeignKey → `BoardGame` | optional, `SET_NULL`, `related_name='fans'` |
| `bio` | TextField | optional |
| `joined_on` | DateField | set automatically |

Methods: `get_absolute_url()`, `initials` property (used for the avatar badge).

### `GameNight` (`nights`)
| Field | Type | Notes |
|---|---|---|
| `title` | CharField | 3+ characters |
| `starts_at` | DateTimeField | |
| `location` | CharField | |
| `max_seats` | PositiveSmallIntegerField | 2-30, includes the host |
| `host` | ForeignKey → `Player` | `PROTECT`, `related_name='hosted_nights'` |
| `games` | ManyToManyField → `BoardGame` | `related_name='game_nights'` |
| `attendees` | ManyToManyField → `Player` | optional, `related_name='attended_nights'` |
| `notes` | TextField | optional |
| `created_at` | DateTimeField | set automatically |

Custom `QuerySet` with `upcoming()` and `past()`, properties `is_upcoming`, `total_players`, `seats_left`.

Queries use `select_related`, `prefetch_related` and `annotate(Count(...))` to avoid extra database hits.

## Forms

Each model has one **base `ModelForm`** with all labels, help texts, placeholders and error messages,
and small forms that inherit from it:

| Model | Create | Edit (read-only field) | Delete (all fields disabled) | Filter |
|---|---|---|---|---|
| BoardGame | `BoardGameCreateForm` | `BoardGameEditForm` (name) | `BoardGameDeleteForm` | `BoardGameFilterForm` |
| Player | `PlayerCreateForm` | `PlayerEditForm` (nickname) | `PlayerDeleteForm` | `PlayerFilterForm` |
| GameNight | `GameNightCreateForm` | `GameNightEditForm` (host) | `GameNightDeleteForm` | `GameNightFilterForm` |

- Automatic fields (`created_at`, `joined_on`) are **excluded**.
- Read-only fields use `disabled = True`, so Django ignores any posted value for them.
- Two reusable mixins in `common/forms.py`: `BootstrapFormMixin` (adds Bootstrap classes to every widget)
  and `ReadOnlyFieldsMixin` (disables the listed fields, or all of them with `'__all__'`).

## Validation rules and messages

| Where | Rule | Message shown |
|---|---|---|
| BoardGame model | name is unique | A game with this name is already on the shelf. |
| BoardGame model | name has 2+ characters | The name must be at least 2 characters long. |
| BoardGame model `clean()` + DB constraint | max players ≥ min players | Maximum players cannot be less than minimum players. |
| BoardGame model | play time 5-600 minutes | A game takes at least 5 minutes. / Games longer than 10 hours are not supported. |
| BoardGame form | image URL is a valid address | Please enter a valid web address starting with http(s):// |
| Player model | nickname is unique | This nickname is already taken. |
| Player model | nickname format | Use only letters, digits and underscores. |
| Player form | full name has no digits | A name cannot contain digits. |
| GameNight model | 2-30 seats | A game night needs at least 2 seats. / That is a party, not a game night (max 30 seats). |
| GameNight form | new night is not in the past | A new game night cannot start in the past. |
| GameNight form | host is not also an attendee | `<host>` is the host and is already counted. |
| GameNight form | everyone fits on the seats | 5 players do not fit on 4 seats. |
| GameNight form | every game supports the group size | Catan supports at most 4 players, but 6 are coming. |
| Player delete view | a host cannot be deleted | `<player>` is hosting game nights. Cancel or re-host them first. |

Required fields also have custom messages, e.g. *"Please give the game a name."*.

## Views

All views are **class-based** (`ListView`, `DetailView`, `CreateView`, `UpdateView`, `DeleteView`).

- Forms are handled with GET (show) and POST (validate and save), then **redirect** to the detail or list
  page (Post/Redirect/Get), with a success message from `SuccessMessageMixin`.
- `FilteredListMixin` (`common/views.py`) validates the filter form and calls `apply_filters()`, which each
  list view implements in its own way.
- `InstanceDeleteFormMixin` (`common/views.py`) passes the object into the disabled delete form so the
  confirmation page shows its data.
- `ProtectedError` is caught when deleting a player who hosts a night, and a friendly error message is shown.
- Unknown objects return **404** (`/games/999/`).

## Templates, filters and tags

- `templates/base.html` - the only base template: Bootstrap layout, navbar, messages and footer.
- 14 page templates: home, 404, and list / detail / form / delete for games, players and nights.
  The create and edit pages share one form template per model.
- Reusable partials in `templates/partials/`: `navbar`, `footer`, `messages`, `form_fields`, `pagination`,
  `game_card`, `night_card`, `player_badge`, `stat_tile`.
- Built-in filters and tags used: `truncatewords`, `timesince`, `timeuntil`, `pluralize`, `date`, `default`,
  `join`, `linebreaksbr`, `widthratio`, `now`, `include ... with`, `for ... empty`.
- Custom filters and tags in `common/templatetags/tabletop_extras.py`:

| Name | Kind | Example |
|---|---|---|
| `duration` | filter | `{{ 95\|duration }}` → `1h 35m` |
| `stars` | filter | `{{ 3\|stars }}` → `★★★☆☆` |
| `get_item` | filter | `{{ stats\|get_item:'Game nights' }}` |
| `url_replace` | simple tag | keeps search / filter / sort when changing pages |
| `stat_tile` | inclusion tag | renders one statistic tile on the home page |

## Tests

```bash
python manage.py test
```

10 tests cover the most important rules: player range text, min/max players, redirects after creating a
game, nickname format, name cleaning, nights in the past, host as attendee, seat limit and the protected
delete of a hosting player.

## Project structure

```
tabletop-nights/
├── manage.py
├── requirements.txt
├── tabletop/                  # project settings and root URLs
├── common/                    # home page, shared mixins, template tags, seed_demo command
│   ├── forms.py               # BootstrapFormMixin, ReadOnlyFieldsMixin
│   ├── views.py               # HomeView, FilteredListMixin, InstanceDeleteFormMixin
│   ├── templatetags/tabletop_extras.py
│   └── management/commands/seed_demo.py   # optional mock data
├── catalog/                   # BoardGame: models, forms, views, urls, tests
├── players/                   # Player: models, forms, views, urls, tests
├── nights/                    # GameNight: models, forms, views, urls, tests
└── templates/
    ├── base.html
    ├── 404.html
    ├── partials/
    ├── common/
    ├── catalog/
    ├── players/
    └── nights/
```

| App | Responsibility |
|---|---|
| `common` | Home page, code shared by all apps, custom template tags, 404, mock data command |
| `catalog` | Board games |
| `players` | Players |
| `nights` | Game nights (depends on `catalog` and `players`) |

## OOP and code quality

- **Inheritance**: base forms per model with create / edit / delete subclasses; shared mixins for forms and views.
- **Abstraction**: `FilteredListMixin.apply_filters()` raises `NotImplementedError` until a subclass implements it.
- **Polymorphism**: each list view filters in its own way through the same `apply_filters()` call.
- **Encapsulation**: business rules live on the models (`supports()`, `seats_left`, `upcoming()`), not in templates.
- **Exception handling**: `ProtectedError` on delete, `TypeError` / `ValueError` in template filters,
  `CommandError` in the demo data command.
- Small apps with one responsibility each; apps talk to each other only through model relations.

## AI usage

AI tools were used to help with the HTML/CSS layout and to structure this README.

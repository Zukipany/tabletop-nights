# 🎲 TableTop Nights

TableTop Nights is a Django web application for groups of friends who play board games together.
Keep a **shelf** of your board games, a list of the **players** in your group, and plan **game nights** -
who hosts, who comes, what gets played and how many seats are left.

The app has no login: everything is managed directly from the UI.

---

## Features

- **Game shelf** - add, browse, search, filter by category, sort and paginate board games.
- **Players** - keep player profiles with experience level and a favourite game.
- **Game nights** - plan nights with a host, attendees and several games; list upcoming or past nights.
- **Smart validation** - e.g. a night cannot start in the past, the host cannot also be an attendee,
  players must fit on the available seats and every selected game must support that many players.
- **Safe deletes** - every delete has a confirmation page showing the object in a read-only form.
  Players who host a night cannot be deleted until the night is cancelled.
- **Dashboard** - home page with live statistics, upcoming nights, newest and most played games.
- **Custom 404 page.**

## Tech stack

- Python 3.12+, Django 6.1
- SQLite
- Bootstrap 5.3 + Bootstrap Icons (loaded from CDN)

## Getting started

```bash
git clone https://github.com/Zukipany/tabletop-nights.git
cd tabletop-nights
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Open http://127.0.0.1:8000/ - the database starts empty. Suggested order for creating data:
**Add game → Add player → Plan a night.**

### Environment variables

None are required. All of them are optional and have safe local defaults:

| Variable | Default | Purpose |
|---|---|---|
| `DJANGO_SECRET_KEY` | an insecure local development key | Secret key |
| `DJANGO_DEBUG` | `False` | Set to `True` to see Django debug pages. With `False` the custom 404 page is shown. |
| `DJANGO_ALLOWED_HOSTS` | `localhost,127.0.0.1` | Comma separated host names |

No credentials are needed.

## Project structure

| App | Responsibility |
|---|---|
| `common` | Home page, shared form mixins, shared view mixins, custom template tags/filters, 404 page |
| `catalog` | `BoardGame` model and its full CRUD |
| `players` | `Player` model and its full CRUD |
| `nights` | `GameNight` model and its full CRUD |

```
tabletop/          project settings and root URLs
common/            home view, mixins, templatetags/tabletop_extras.py
catalog/           board games
players/           players
nights/            game nights
templates/         base.html, 404.html, partials/ and one folder per app
```

## Database design

| Model | Key fields | Relationships |
|---|---|---|
| `BoardGame` | name (unique), category, min/max players, play time, complexity | - |
| `Player` | nickname (unique), full name, skill level | **many-to-one** → `BoardGame` (favourite game) |
| `GameNight` | title, start time, location, seats | **many-to-one** → `Player` (host), **many-to-many** → `BoardGame` (games), **many-to-many** → `Player` (attendees) |

Extras: `TextChoices`/`IntegerChoices`, a database `CheckConstraint` (max players ≥ min players),
model `clean()`, validators with custom messages, a custom `QuerySet` (`upcoming()` / `past()`),
`select_related` / `prefetch_related` / `annotate(Count(...))` queries.

## Pages

| Page | URL |
|---|---|
| Home (dashboard) | `/` |
| Game list (search / filter / sort) · details · add · edit · delete | `/games/` |
| Player list (search / filter) · details · add · edit · delete | `/players/` |
| Game night list (upcoming / past / search) · details · plan · edit · cancel | `/nights/` |
| Custom 404 | any unknown URL |

## Forms

- Create / edit / delete forms for each model, built on a shared base form per model.
- Edit forms show identity fields as **read-only** (game name, player nickname, night host).
- Delete confirmation forms are fully disabled.
- Filter forms for each list page.
- Custom labels, help texts, placeholders and error messages; `exclude` hides auto fields.

## Templates

- `base.html` with navbar and footer partials on every page.
- Reusable partials: game card, night card, player badge, form fields, pagination, messages, stat tile.
- Custom template filters `duration`, `stars`, `get_item`; custom tags `url_replace` (simple tag) and
  `stat_tile` (inclusion tag).

## AI usage

AI tools were used to help with the HTML/CSS layout and to structure this README.

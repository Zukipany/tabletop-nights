"""Custom template filters and tags used across the site."""
from django import template

register = template.Library()


@register.filter
def duration(minutes):
    """Turns a number of minutes into a friendly string: 95 -> '1h 35m'."""
    try:
        minutes = int(minutes)
    except (TypeError, ValueError):
        return ''
    hours, rest = divmod(minutes, 60)
    if hours and rest:
        return f'{hours}h {rest}m'
    return f'{hours}h' if hours else f'{rest}m'


@register.filter
def stars(value, maximum=5):
    """Renders a rating as stars: 3 -> '★★★☆☆'."""
    try:
        value = int(value)
    except (TypeError, ValueError):
        value = 0
    return '★' * value + '☆' * (int(maximum) - value)


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    """Keeps the current GET parameters and overrides the given ones (for sorting/pagination)."""
    params = context['request'].GET.copy()
    for key, value in kwargs.items():
        params[key] = value
    return params.urlencode()


@register.inclusion_tag('partials/stat_tile.html')
def stat_tile(label, value, icon='dice-5'):
    """Renders one statistic tile on the home page."""
    return {'label': label, 'value': value, 'icon': icon}


@register.filter
def get_item(mapping, key):
    """Looks up a dictionary key that contains spaces: {{ stats|get_item:'Game nights' }}."""
    return mapping.get(key, '') if hasattr(mapping, 'get') else ''

from django import template

register = template.Library()


@register.filter
def star_range(value):
    try:
        return range(int(value))
    except (TypeError, ValueError):
        return range(0)


@register.filter
def empty_star_range(value):
    try:
        value = int(value)
        return range(max(0, 5 - value))
    except (TypeError, ValueError):
        return range(5)
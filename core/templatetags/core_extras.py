from django import template

register = template.Library()


@register.filter
def star_range(rating):
    return range(rating)
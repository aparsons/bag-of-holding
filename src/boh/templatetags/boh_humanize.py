from datetime import date

from django import template
from django.utils.timesince import timesince, timeuntil

register = template.Library()


@register.filter(name='humanize_date')
def humanize_date(value):
    today = date.today()
    try:
        if value > today:
            return 'In ' + timeuntil(value)
        elif value < today:
            return timesince(value) + ' ago'
        else:
            return 'Today'
    except (ValueError, TypeError):
        return ''

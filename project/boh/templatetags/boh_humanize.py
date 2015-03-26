from datetime import date

from django import template
from django.utils.timesince import timesince, timeuntil

register = template.Library()

@register.filter(name='humanize_date')
def humanize_date(value):
    try:
        if value >= date.today():
            return 'In ' + timeuntil(value)
        else:
            return timesince(value) + ' ago'
    except (ValueError, TypeError):
        return ''

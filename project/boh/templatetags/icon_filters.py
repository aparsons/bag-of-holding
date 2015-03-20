from django import template
from django.utils.safestring import mark_safe

from boh.models import Application

register = template.Library()

def icon(name, tooltip):
    return '<span class="fa fa-' + name + '" aria-hidden="true" data-toggle="tooltip" title="' + tooltip + '"></span>'

@register.filter
def platform_icon(value):
    if value == Application.WEB_PLATFORM:
        return mark_safe(icon('list-alt','Web'))
    elif value == Application.DESKTOP_PLATFORM:
        return mark_safe(icon('desktop','Desktop'))
    elif value == Application.MOBILE_PLATFORM:
        return mark_safe(icon('mobile','Mobile'))
    elif value == Application.WEB_SERVICE_PLATFORM:
        return mark_safe(icon('plug','Web Service'))
    else:
        return mark_safe(icon('question','Not Specified'))

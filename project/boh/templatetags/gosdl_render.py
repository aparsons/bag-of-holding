# https://docs.djangoproject.com/en/1.11/howto/custom-template-tags/

from django import template
from django.utils.safestring import mark_safe

from ..gosdl import GoSDL

register = template.Library()


@register.filter
def gosdl_render(value):
    return mark_safe(str(GoSDL.from_json(value)))

from django import template
from django.utils.safestring import mark_safe

from ..models import Application


register = template.Library()


def icon(name, tooltip):
    return '<span class="fa fa-' + name + ' fa-fw" aria-hidden="true" data-toggle="tooltip" data-placement="bottom" title="' + tooltip + '"></span>'


def not_specified_icon(tooltip):
    return '<span class="fa fa-question fa-fw text-danger" aria-hidden="true" data-toggle="tooltip" data-placement="bottom" title="' + tooltip + '"></span>'


def stars(filled, total, tooltip):
    code = '<span data-toggle="tooltip" data-placement="bottom" title="' + tooltip + '">'
    for i in range(0, total):
        if i < filled:
            code += '<span class="fa fa-star" aria-hidden="true"></span>'
        else:
            code += '<span class="fa fa-star-o text-muted" aria-hidden="true"></span>'
    code += '</span>'
    return code

@register.filter
def business_criticality_icon(value):
    if value == Application.VERY_HIGH_CRITICALITY:
        return mark_safe(stars(5, 5, 'Very High'))
    if value == Application.HIGH_CRITICALITY:
        return mark_safe(stars(4, 5, 'High'))
    if value == Application.MEDIUM_CRITICALITY:
        return mark_safe(stars(3, 5, 'Medium'))
    if value == Application.LOW_CRITICALITY:
        return mark_safe(stars(2, 5, 'Low'))
    if value == Application.VERY_LOW_CRITICALITY:
        return mark_safe(stars(1, 5, 'Very Low'))
    if value == Application.NONE_CRITICALITY:
        return mark_safe(stars(0, 5, 'None'))
    else:
        return mark_safe(not_specified_icon('Business Criticality Not Specified'))


@register.filter
def platform_icon(value):
    if value == Application.WEB_PLATFORM:
        return mark_safe(icon('list-alt', 'Web'))
    elif value == Application.DESKTOP_PLATFORM:
        return mark_safe(icon('desktop', 'Desktop'))
    elif value == Application.MOBILE_PLATFORM:
        return mark_safe(icon('mobile', 'Mobile'))
    elif value == Application.WEB_SERVICE_PLATFORM:
        return mark_safe(icon('plug', 'Web Service'))
    else:
        return mark_safe(not_specified_icon('Platform Not Specified'))


@register.filter
def lifecycle_icon(value):
    if value == Application.IDEA_LIFECYCLE:
        return mark_safe(icon('lightbulb-o', 'Idea'))
    if value == Application.EXPLORE_LIFECYCLE:
        return mark_safe(icon('compass', 'Explore'))
    if value == Application.VALIDATE_LIFECYCLE:
        return mark_safe(icon('search', 'Validate'))
    if value == Application.GROW_LIFECYCLE:
        return mark_safe(icon('leaf', 'Grow'))
    if value == Application.SUSTAIN_LIFECYCLE:
        return mark_safe(icon('ship', 'Sustain'))
    if value == Application.RETIRE_LIFECYCLE:
        return mark_safe(icon('moon-o', 'Retire'))
    else:
        return mark_safe(not_specified_icon('Lifecycle Not Specified'))


@register.filter
def origin_icon(value):
    if value == Application.THIRD_PARTY_LIBRARY_ORIGIN:
        return mark_safe(icon('book', 'Third-Party Library'))
    if value == Application.PURCHASED_ORIGIN:
        return mark_safe(icon('money', 'Purchased'))
    if value == Application.CONTRACTOR_ORIGIN:
        return mark_safe(icon('suitcase', 'Contractor Developed'))
    if value == Application.INTERNALLY_DEVELOPED_ORIGIN:
        return mark_safe(icon('home', 'Internally Developed'))
    if value == Application.OPEN_SOURCE_ORIGIN:
        return mark_safe(icon('code', 'Open Source'))
    if value == Application.OUTSOURCED_ORIGIN:
        return mark_safe(icon('globe', 'Outsourced'))
    else:
        return mark_safe(not_specified_icon('Origin Not Specified'))


@register.filter
def external_audience_icon(value):
    if value:
        return mark_safe(icon('users', 'External Audience'))
    else:
        return ''


@register.filter
def internet_accessible_icon(value):
    if value:
        return mark_safe(icon('cloud', 'Internet Accessible'))
    else:
        return ''
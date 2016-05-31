import phonenumbers

from django import template

register = template.Library()


@register.filter(name='format_phone')
def format_phone(value):
    if value:
        number = phonenumbers.parse(value, 'US')
        return phonenumbers.format_number(number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
    else:
        return ''

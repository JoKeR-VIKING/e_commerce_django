import locale
from django import template
from dateutil import tz
from datetime import datetime

register = template.Library()

@register.filter()
def replaceChar(value, arg):
    arg = arg.split(',')
    return value.replace(arg[0], arg[1])

@register.filter()
def indianPrice(value):
    locale.setlocale(locale.LC_MONETARY, 'en_IN')
    return locale.currency(value, grouping=True)


from django import template

register = template.Library()
CURRENCIES_SYMBOLS = {
   'омске': '**',
   }

@register.filter()
def censor(code = "омске"):
    simb = CURRENCIES_SYMBOLS[code]
    return f'{simb}'

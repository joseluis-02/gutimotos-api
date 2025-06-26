from babel.numbers import format_decimal
from decimal import Decimal

def format_currency_locale(value):
    if not isinstance(value, Decimal):
        value = Decimal(value)
    return format_decimal(value,locale='es_BO')

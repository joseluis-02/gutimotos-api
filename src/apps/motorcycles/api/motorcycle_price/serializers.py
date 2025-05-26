# Django rest framework
from rest_framework import serializers
# Babel
from babel.numbers import format_decimal
# Functions
from ...functions.format_currency_locale import format_currency_locale

# Serializer CalculatedPriceByCurrencySerializer
class CalculatedPriceByCurrencySerializer(serializers.Serializer):
    currency = serializers.CharField()
    final_price = serializers.SerializerMethodField()
    def get_final_price(self, obj):
        return format_currency_locale(obj['final_price'])
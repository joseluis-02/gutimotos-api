# Django rest framework
from rest_framework import serializers
# Models
from ...models.currency import Currency

class CurrencyModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ["code", "name", "symbol"]
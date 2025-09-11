# Django rest framework
from rest_framework import serializers
# Models
from ...models.type_price import TypePrice

class TypePriceModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypePrice
        fields = ["slug", "name"]
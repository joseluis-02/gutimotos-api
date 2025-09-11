# Django REST Framework
from rest_framework import serializers

class MotorcyclePriceByMotorcycleTypeSerializer(serializers.Serializer):
    currency_name = serializers.CharField()
    currency_code = serializers.CharField()
    final_price = serializers.DecimalField(max_digits=12, decimal_places=2)
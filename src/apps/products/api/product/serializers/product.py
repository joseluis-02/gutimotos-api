# Django rest framework
from rest_framework import serializers
# Models
from ....models import Product

class ProductListSerializer(serializers.ModelSerializer):
    brand = serializers.SerializerMethodField()
    country = serializers.SerializerMethodField()
    category_description = serializers.CharField(source='category.description_sin', read_only=True)
    measure_short_name = serializers.CharField(source='measure.short_name', read_only=True)
    class Meta:
        model = Product
        fields = [
            'id', 'code', 'description',
            'brand', 'country',
            'category_description', 'measure_short_name'
        ]

    def get_brand(self, obj):
        return obj.brand.name if obj.brand else ''

    def get_country(self, obj):
        return obj.country.code if obj.country else ''

# Django rest framework
from rest_framework import serializers
# Models
from ...models.product import Product

class ProductListSerializer(serializers.ModelSerializer):
    brand = serializers.SerializerMethodField()
    country = serializers.SerializerMethodField()
    measure_short_name = serializers.CharField(source='measure.short_name', read_only=True)
    class Meta:
        model = Product
        fields = [
            'id', 'code', 'description',
            'brand', 'country', 'measure_short_name'
        ]

    def get_brand(self, obj):
        return obj.brand.name if obj.brand else ''

    def get_country(self, obj):
        return obj.country.code if obj.country else ''

class ProductTabulatorModelSerializer(serializers.ModelSerializer):
    brand_name = serializers.SerializerMethodField()
    category = serializers.CharField(source="category.description_sin")
    price = serializers.SerializerMethodField()
    currency = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ("id", "code", "description", "brand_name", "category", "price", "currency")
        
    def get_brand_name(self, obj):
        return obj.brand.name if obj.brand else None
    def get_price(self, obj):
        currency_code = self.context.get("currency")
        type_price = self.context.get("type_price")

        price_obj = next((p for p in obj.p_prices.all() if p.currency.code == currency_code), None)
        if not price_obj:
            return None

        if type_price:
            return round(price_obj.base * (1 + type_price.profit_margin / 100), 2)
        return price_obj.base

    def get_currency(self, obj):
        price = self.get_price(obj)
        return self.context.get("currency") if price is not None else None
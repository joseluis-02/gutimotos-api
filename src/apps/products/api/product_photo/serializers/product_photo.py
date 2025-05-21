# Python
from decimal import Decimal,ROUND_HALF_UP
# Django rest framewok
from rest_framework import serializers
# Models
from apps.products.models import ProductPhoto

# 
class ProductPhotoListSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    sale_price = serializers.SerializerMethodField()
    currency = serializers.SerializerMethodField()

    class Meta:
        model = ProductPhoto
        fields = ['id', 'product_id','image_url', 'sale_price', 'currency']

    def get_image_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.image_url.url) if request else obj.image_url.url

    def get_sale_price(self, obj):
        margin = self.context.get('profit_margin')  # Debes pasar esto desde la View
        if margin is None:
            return None

        prices = getattr(obj.product, 'filtered_prices', [])
        if prices:
            price_obj = prices[0]  # Solo debería haber uno
            base = price_obj.base
            sale_price = base + (base * Decimal(margin) / Decimal('100'))
            return str(sale_price.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))
        return None

    def get_currency(self, obj):
        prices = getattr(obj.product, 'filtered_prices', [])
        if prices and prices[0].currency:
            return prices[0].currency.code
        return None

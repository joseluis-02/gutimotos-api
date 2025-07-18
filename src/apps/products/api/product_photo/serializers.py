# Django rest framework
from rest_framework import serializers
# Models
from ...models.product_photo import ProductPhoto

class ProductPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPhoto
        fields = ('__all__')

class ProductPhotoListSerializer(serializers.ModelSerializer):
    product_code = serializers.SerializerMethodField()

    class Meta:
        model = ProductPhoto
        fields = [
            'id',
            'product',
            'photo',
            'product_code',
        ]

    def get_product_code(self, obj):
        code = obj.product.code
        currency_code = self.context.get("currency")
        type_price = self.context.get("type_price")

        price_obj = next(
            (p for p in obj.product.p_prices.all() if p.currency.code == currency_code),
            None
        )

        if not price_obj:
            return code
        if not type_price:
            return code
        return f"{code} ({currency_code} {round(price_obj.base * (1 + type_price.profit_margin / 100), 2)})"

class ProductPhotoDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPhoto
        fields = ['id', 'photo']
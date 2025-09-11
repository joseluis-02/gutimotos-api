# Django rest framework
from rest_framework import serializers
# Models
from ...models.product_photo import ProductPhoto

class ProductPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPhoto
        fields = ('__all__')

class ProductPhotoListSerializer(serializers.ModelSerializer):
    calculated_price = serializers.SerializerMethodField()
    product_description = serializers.CharField(source="product.description", read_only=True)
    product_code = serializers.CharField(source="product.code", read_only=True)

    class Meta:
        model = ProductPhoto
        fields = [
            'id',
            'product',
            'photo',
            'product_code',
            'product_description',
            'calculated_price',
        ]

    def get_calculated_price(self, obj):
        currency_code = self.context.get("currency_code")
        type_price = self.context.get("type_price")

        # Obtener el precio base en la moneda seleccionada
        price_obj = next(
            (p for p in obj.product.p_prices.all() if p.currency.code == currency_code),
            None
        )

        if not price_obj or not type_price:
            return None

        # Usar la función escalonada del modelo
        final_price = type_price.calculate_price_product_scaled_tranches(price_obj.base)

        return int(final_price)

class ProductPhotoDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPhoto
        fields = ['id', 'photo']
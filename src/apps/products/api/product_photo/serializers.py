# Django rest framework
from rest_framework import serializers
# Models
from ...models.product_photo import ProductPhoto
# Choices
from apps.core.choices.product_type import ProductType
class ProductPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPhoto
        fields = ('__all__')

class ProductPhotoListSerializer(serializers.ModelSerializer):
    calculated_price = serializers.SerializerMethodField()
    brand_name = serializers.SerializerMethodField()
    measure_name = serializers.CharField(source="product.measure.name", read_only=True)
    product_description = serializers.CharField(source="product.description", read_only=True)
    product_code = serializers.CharField(source="product.code", read_only=True)

    class Meta:
        model = ProductPhoto
        fields = [
            'id',
            'product',
            'photo',
            'brand_name',
            'measure_name',
            'product_code',
            'product_description',
            'calculated_price',
        ]
    def get_brand_name(self, obj):
        return obj.product.brand.name if obj.product.brand else None
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
        final_price = type_price.calculate_price(price_obj.base, ProductType.SPAREPART)

        return int(final_price)

class ProductPhotoDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPhoto
        fields = ['id', 'photo']
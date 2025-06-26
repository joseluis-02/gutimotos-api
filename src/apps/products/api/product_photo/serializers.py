# Django rest framework
from rest_framework import serializers
# Models
from ...models.product_photo import ProductPhoto

class ProductPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPhoto
        fields = ('__all__')

class ProductPhotoListSerializer(serializers.ModelSerializer):
    product_code = serializers.CharField(source='product.code')
    class Meta:
        model = ProductPhoto
        fields = [
            'id',
            'product',
            'photo',
            'product_code',
        ]
    

class ProductPhotoDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPhoto
        fields = ['id', 'photo']
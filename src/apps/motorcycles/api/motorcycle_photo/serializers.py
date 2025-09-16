# Django rest-framework
from rest_framework import serializers
# Models
from ...models.motorcycle_photo import MotorcyclePhoto
class MotorcyclePhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MotorcyclePhoto
        fields = ('__all__')

class MotorcyclePhotoListSerializer(serializers.ModelSerializer):
    brand = serializers.CharField(source='motorcycle_file.brand.name')
    motorcycle_type = serializers.CharField(source='motorcycle_file.motorcycle_type.get_full_path')
    color = serializers.CharField(source='motorcycle_file.color.name')
    class Meta:
        model = MotorcyclePhoto
        fields = [
            'id',
            'photo',
            'brand',
            'motorcycle_type',
            'color',
            'created',
        ]
    

class MotorcyclePhotoDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = MotorcyclePhoto
        fields = ['id', 'photo']
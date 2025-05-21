# Django
from django.db import models
# Django rest-framework
from rest_framework import serializers
# Models
from ....models import MotorcyclePhoto
# Choices
from apps.motorcycles.choices import SideDirection
# Modelo MotorcyclePhoto=MotocicletaFoto
class MotorcyclePhotoMinimalSerializer(serializers.ModelSerializer):
    motorcycle_type_name = serializers.CharField(source='motorcycle_type.get_full_path', read_only=True)
    color_name = serializers.CharField(source='color.name', read_only=True)
    brand_name = serializers.CharField(source='brand.name', read_only=True)
    class Meta:
        model = MotorcyclePhoto
        fields = ['motorcycle_type', 'brand','color', 'motorcycle_type_name', 'color_name','brand_name', 'image_url']

# Serializador completo (para obtener todos los datos)
class MotorcyclePhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MotorcyclePhoto
        fields = '__all__'
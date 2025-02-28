# Django
from django.db import models
# Django rest-framework
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
# Models
from apps.motorcycles.models import Brand, MotorcyclePhoto
# Choices
from apps.motorcycles.choices import SideDirection
# Serializador del modelo Brand=Marca
class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'
# Modelo MotorcyclePhoto=MotocicletaFoto
class MotorcyclePhotoMinimalSerializer(serializers.ModelSerializer):
    motorcycle_type_name = serializers.CharField(source='motorcycle_type.get_full_path', read_only=True)
    color_name = serializers.CharField(source='color.name', read_only=True)
    class Meta:
        model = MotorcyclePhoto
        fields = ['motorcycle_type', 'color', 'motorcycle_type_name', 'color_name', 'image_url']

# Serializador completo (para obtener todos los datos)
class MotorcyclePhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MotorcyclePhoto
        fields = '__all__'
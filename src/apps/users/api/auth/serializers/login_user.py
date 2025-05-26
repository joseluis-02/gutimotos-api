# Django rest-framework
from rest_framework import serializers

# Serializer para Iniciar sesión de usuario con email y contraseña
class LoginUserSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

# Django rest-framework
from rest_framework import serializers

# Serializer para iniciar sesión de usuario con token social
class LoginSocialSerializer(serializers.Serializer):
    token_social = serializers.CharField(required=True)

# Django rest-framework
from rest_framework import serializers

# Serializer para logout de usuario
class LogoutUserSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(required=True)

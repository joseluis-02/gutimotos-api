from rest_framework import serializers
from .models import AuthToken

class AuthTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthToken
        fields = ['access_token', 'refresh_token']
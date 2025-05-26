# Django rest framework
from rest_framework import serializers
# Models
from ....models import User
# User List serializer
class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'is_active', 'created']
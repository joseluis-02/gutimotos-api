# apps/users/api/serializers/update.py
from rest_framework import serializers
from apps.users.models import User

class UserUpdateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=False)
    password = serializers.CharField(required=False, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ("email", "password")

    def validate_email(self, value):
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError("Este correo ya está en uso.")
        return value

    def update(self, instance, validated_data):
        if "email" in validated_data:
            instance.email = validated_data["email"]
        if "password" in validated_data:
            instance.set_password(validated_data["password"])
        instance.save()
        return instance

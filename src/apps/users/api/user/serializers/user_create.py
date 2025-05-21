# Django rest-framework
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
# Models
from ....models import User

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        min_length=8,
        error_messages={
            "min_length": "La contraseña debe tener al menos 8 caracteres.",
            "blank": "La contraseña no puede estar vacía.",
        }
    )
    email = serializers.EmailField(
        required=True,
        error_messages={
            "invalid": "Ingresa un correo electrónico válido.",
            "blank": "El correo es requerido."
        }
    )

    class Meta:
        model = User
        fields = ("email", "password")

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Este correo ya está registrado.")
        return value

    def create(self, validated_data):
        return User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"]
        )

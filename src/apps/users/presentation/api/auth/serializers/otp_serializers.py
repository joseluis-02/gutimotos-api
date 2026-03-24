# Django rest
from rest_framework import serializers

class RequestOTPSerializer(serializers.Serializer):
    """Serializer para solicitar código OTP"""
    
    email = serializers.EmailField(
        required=True,
        help_text='Email del usuario'
    )
    
    def validate_email(self, value):
        """Normaliza el email"""
        return value.lower().strip()


class VerifyOTPSerializer(serializers.Serializer):
    """Serializer para verificar código OTP"""
    
    email = serializers.EmailField(
        required=True,
        help_text='Email del usuario'
    )
    
    code = serializers.CharField(
        min_length=6,
        max_length=6,
        required=True,
        help_text='Código OTP de 6 dígitos'
    )
    
    def validate_email(self, value):
        """Normaliza el email"""
        return value.lower().strip()
    
    def validate_code(self, value):
        """Valida que sea numérico"""
        if not value.isdigit():
            raise serializers.ValidationError(
                "El código debe contener solo números"
            )
        return value.strip()
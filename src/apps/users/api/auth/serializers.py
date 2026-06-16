# Django REST Framework
from rest_framework import serializers
# Simple JWT
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

# ---------------------------------------------------
# Base: utilidades comunes para validación de tokens
# ---------------------------------------------------
class TokenValidatorMixin:
    ERROR_MESSAGES = {
        "required": "El refresh token es requerido.",
        "blank": "El refresh token no puede estar vacío.",
        "blacklisted": "El refresh token ya fue cerrado.",
        "expired": "El refresh token ha expirado.",
        "invalid": "Refresh token inválido.",
    }

    def validate_refresh_token_value(self, value: str) -> str:
        try:
            RefreshToken(value)  # valida firma, expiración y que sea un refresh válido
        except TokenError as e:
            msg = str(e).lower()
            if "blacklisted" in msg:
                raise serializers.ValidationError(self.ERROR_MESSAGES["blacklisted"])
            elif "expired" in msg:
                raise serializers.ValidationError(self.ERROR_MESSAGES["expired"])
            else:
                raise serializers.ValidationError(self.ERROR_MESSAGES["invalid"])
        return value


# ---------------------------------------------------
# Serializers específicos
# ---------------------------------------------------
class AuthGoogleSerializer(serializers.Serializer):
    """Serializer para inicio de sesión con token de Google/Firebase."""
    token = serializers.CharField(
        required=True,
        allow_blank=False,
        error_messages={
            "blank": "Debe enviar el token Google del usuario obtenido de Firebase por el body con el nombre 'token'.",
            "required": "Debe enviar el token Google del usuario obtenido de Firebase por el body con el nombre 'token'."
        }
    )


class AuthLogoutSerializer(TokenValidatorMixin, serializers.Serializer):
    """Serializer para cierre de sesión con refresh token."""
    refresh_token = serializers.CharField(
        required=True,
        allow_blank=False,
        error_messages=TokenValidatorMixin.ERROR_MESSAGES
    )

    def validate_refresh_token(self, value: str) -> str:
        return self.validate_refresh_token_value(value)


class AuthRefreshTokenSerializer(TokenValidatorMixin, serializers.Serializer):
    """Serializer para renovar access token a partir de un refresh válido."""
    refresh_token = serializers.CharField(
        required=True,
        allow_blank=False,
        error_messages=TokenValidatorMixin.ERROR_MESSAGES
    )

    def validate_refresh_token(self, value: str) -> str:
        return self.validate_refresh_token_value(value)


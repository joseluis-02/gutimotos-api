# SimpleJWT
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        """
        Personaliza el contenido del token JWT agregando solo lo esencial.
        Este método define qué se incluye en el payload del JWT.
        """
        token = super().get_token(user)

        # Añadir campos personalizados al payload (cuidado con no incluir datos sensibles)
        token['id'] = str(user.id)
        token['email'] = user.email
        return token

    def validate(self, attrs):
        """
        Este método valida las credenciales y personaliza la respuesta del login,
        añadiendo detalles del usuario junto con los tokens generados.
        """
        data = super().validate(attrs)  # data = {'access': ..., 'refresh': ...}

        # Agregar datos adicionales del usuario a la respuesta JSON (no al token)
        data['user'] = {
            'id': str(self.user.id),
            'email': self.user.email,
            'email_verified': getattr(self.user, 'email_verified', False)
        }

        return data
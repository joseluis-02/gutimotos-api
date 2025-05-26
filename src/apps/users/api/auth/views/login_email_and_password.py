# Django
from django.contrib.auth import authenticate
# Django rest-framework
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
# SimpleJWT
from rest_framework_simplejwt.tokens import RefreshToken
# Serializers
from ..serializers import LoginUserSerializer
# Functions
from ....functions import set_jwt_cookies

# Función para iniciar sesión con email y contraseña
class LoginEmailAndPasswordAPIView(APIView):
    serializer_class = LoginUserSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Obtener las credenciales de inicio de sesión
        email = serializer.data.get('email')
        password = serializer.data.get('password')
        # Verificamos si el usuario existe
        user = authenticate(email=email, password=password)
        if user is not None and user.is_active:
            if user.is_active == False:
                return Response({'error': 'Usuario se encuentra inactivo'}, status=status.HTTP_403_FORBIDDEN)
            # Crear un nuevo refresh token para el usuario
            refresh = RefreshToken.for_user(user)
            # Crear un access token
            access = refresh.access_token
            # Aquí personalizamos el access token agregando información adicional
            access['id'] = str(user.id)
            access['email'] = user.email
            access['is_active'] = user.is_active
            access['email_verified'] = user.email_verified
            #access['full_name'] = f"{user.first_name} {user.last_name}"  # Ejemplo de nombre completo
            # Generar la respuesta con los tokens y datos adicionales
            response = Response({
                'refresh': str(refresh),
                'access': str(access),
                'user': {
                    'id': str(user.id),
                    'email': user.email,
                    'email_verified': user.email_verified,
                }
            }, status=status.HTTP_200_OK)
            # Añadir las cookies JWT (esto se configura en tu función set_jwt_cookies)
            return set_jwt_cookies(response, access, refresh)
        else:
            return Response({'error': 'Usuario con credenciales incorrectos'}, status=status.HTTP_400_BAD_REQUEST)

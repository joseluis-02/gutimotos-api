# Django rest-framework
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
# SimpleJWT
from rest_framework_simplejwt.tokens import RefreshToken
# Firebase admin
from firebase_admin import auth
# Serializers
from ..serializers import LoginSocialSerializer
# Models
from ....models import User
# functions
from ....functions import set_jwt_cookies

# Función para entrar con la cuenta de Google
class LoginGoogleAPIView(APIView):
    serializer_class = LoginSocialSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Recuperar la información del token de acceso de Google
        token_google = serializer.data.get('token_google')
        # Verificamos el token con Firebase Admin SDK
        try:
            decode_access_token = auth.verify_id_token(token_google)
        except Exception as e:
            return Response({"error": "Token de Google no válido"}, status=status.HTTP_401_UNAUTHORIZED)

        # Extraer la información del token decodificado
        email = decode_access_token.get('email')
        name = decode_access_token.get('name')
        picture = decode_access_token.get('picture')
        email_verified = decode_access_token.get('email_verified')

        # Verificamos si el correo electrónico está verificado por Google
        if not email_verified:
            return Response({"error": "Email no verificado por Google"}, status=status.HTTP_400_BAD_REQUEST)
        # Buscar o crear usuario
        user, _ = User.objects.get_or_create(
            email=email, 
            defaults={
                'email_verified': email_verified,
                'is_active': True,
                }
            )
        if user is not None:
            if user.is_active == False:
                return Response({'error': 'Usuario se encuentra inactivo'}, status=status.HTTP_403_FORBIDDEN)

            # Crear un nuevo refresh token para el usuario
            refresh = RefreshToken.for_user(user)

            # Crear un access token
            access = refresh.access_token

            # Aquí personalizamos el access token agregando información adicional
            access['id'] = str(user.id)  # Puedes agregar cualquier campo personalizado
            access['email'] = user.email
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
            return Response({'error': 'Usuario de google no válido'}, status=status.HTTP_400_BAD_REQUEST)

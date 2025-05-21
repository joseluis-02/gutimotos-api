# Django rest-framework
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
# SimpleJWT
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework_simplejwt.authentication import JWTAuthentication
# Serializers
from ..serializers import LogoutUserSerializer

# Función para cerrar sesión y eliminar cookies
class LogoutAPIView(APIView):
    serializer_class = LogoutUserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Obtener el refresh token ya sea desde cookie o body
        refresh_token = request.COOKIES.get('refresh_token') or request.data.get('refresh_token')
        #print(refresh_token)
        if not refresh_token:
            return Response(
                {'error': 'No se encontró el token de actualización (refresh token).'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except TokenError:
            return Response(
                {'error': 'Token inválido o ya ha sido cerrado.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Limpieza de cookies
        response = Response({'message': 'Sesión cerrada correctamente.'}, status=status.HTTP_205_RESET_CONTENT)
        response.delete_cookie('refresh_token')
        response.delete_cookie('access_token')
        return response

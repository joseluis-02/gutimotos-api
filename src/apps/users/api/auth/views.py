# Django
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.conf import settings
# DRF
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny,IsAdminUser
from rest_framework.exceptions import ValidationError, AuthenticationFailed
# JWT
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import TokenError
# Serializers
from .serializers import AuthGoogleSerializer, AuthLogoutSerializer, AuthRefreshTokenSerializer
# Functions & Services
from .functions import set_jwt_cookies, create_new_refresh_token, validate_refresh_token, cleanup_outstanding_tokens, cleanup_blacklisted_tokens
from .services import verify_google_token


User = get_user_model()


# ---------------------------------------------------
# BaseView con helpers unificados
# ---------------------------------------------------
class BaseAuthAPIView(APIView):
    """Base para vistas de autenticación con helpers de respuesta unificada."""

    def _response_success(self, message, data=None, status_code=200):
        return Response({"success": True, "message": message, "data": data}, status=status_code)

    def _response_error(self, message, status_code=400):
        return Response({"success": False, "message": message, "data": None}, status=status_code)

    def handle_exception(self, exc):
        if isinstance(exc, ValidationError):
            detail = exc.detail
            if isinstance(detail, dict):
                message = "; ".join([str(v[0]) for v in detail.values()])
            elif isinstance(detail, list):
                message = detail[0]
            else:
                message = str(detail)
            return self._response_error(message, 400)

        if isinstance(exc, AuthenticationFailed):
            return self._response_error("No autorizado o token inválido.", 401)

        if isinstance(exc, TokenError):
            msg = str(exc).lower()
            if "blacklisted" in msg:
                message = "El refresh token ya fue cerrado."
            elif "expired" in msg:
                message = "El refresh token ha expirado."
            else:
                message = "Refresh token inválido."
            return self._response_error(message, 400)

        return self._response_error(str(exc), 400)


# ---------------------------------------------------
# Google Login
# ---------------------------------------------------
@method_decorator(csrf_exempt, name="dispatch")
class AuthGoogleAPIView(BaseAuthAPIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = AuthGoogleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data["token"]

        try:
            user_data = verify_google_token(token)
        except ValueError:
            return self._response_error("Token de Google inválido o expirado.", 400)

        user, created = User.objects.get_or_create(
            email=user_data["email"],
            defaults={
                "auth_uid": user_data.get("auth_uid"),
                "email_verified": user_data.get("email_verified", False),
                "auth_provider": user_data.get("auth_provider", "google"),
                "is_active": True,
            }
        )

        if not user.is_active:
            return self._response_error("Usuario se encuentra inactivo", 403)

        refresh, access = create_new_refresh_token(user)

        data = {
            "access": str(access),
            "refresh": str(refresh),
            "user": {
                "id": str(user.id),
                "email": user.email,
                "email_verified": user.email_verified,
            }
        }

        response = self._response_success("Usuario creado e inicio de sesión exitoso" if created else "Inicio de sesión exitoso", data)
        return set_jwt_cookies(response, access, refresh, request=request)


# ---------------------------------------------------
# Logout
# ---------------------------------------------------
class AuthLogoutAPIView(BaseAuthAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        serializer = AuthLogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        refresh_token_str = serializer.validated_data.get("refresh_token")

        # Blacklistear el refresh token
        if refresh_token_str:
            try:
                refresh = RefreshToken(refresh_token_str)
                refresh.blacklist()
            except TokenError:
                pass

        # Limpiar cookies
        response = self._response_success("Sesión cerrada correctamente", None, status.HTTP_205_RESET_CONTENT)
        for cookie_name in ["access_token", "refresh_token", "csrftoken"]:
            response.delete_cookie(cookie_name, path="/")
        return response


# ---------------------------------------------------
# Refresh token
# ---------------------------------------------------
class AuthRefreshTokenAPIView(BaseAuthAPIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = AuthRefreshTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        refresh_token_str = serializer.validated_data["refresh_token"]

        try:
            refresh = validate_refresh_token(refresh_token_str)
        except TokenError as e:
            return self._response_error(str(e), 400)

        # ✅ solo aquí se crea un access token si es válido y no está en blacklist
        access = refresh.access_token

        return self._response_success(
            "Access token renovado correctamente",
            {"access": str(access)},
            200
        )

class TokenCleanupAPIView(APIView):
    """
    Endpoint para limpiar tokens expirados.
    Solo accesible para administradores.
    """
    #permission_classes = [IsAdminUser]

    def post(self, request):
        deleted_outstanding = cleanup_outstanding_tokens()
        deleted_blacklisted = cleanup_blacklisted_tokens()

        return Response({
            "success": True,
            "message": "Tokens expirados limpiados correctamente",
            "data": {
                "outstanding_deleted": deleted_outstanding,
                "blacklisted_deleted": deleted_blacklisted
            }
        }, status=status.HTTP_200_OK)


# Django
from django.http import Http404
from django.core.exceptions import PermissionDenied
# Django rest framework
from rest_framework import status
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated, ValidationError
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

def custom_exception_handler(exc, context):
    # Obtener la respuesta original de DRF
    response = exception_handler(exc, context)

    # Valores por defecto
    message = str(exc)
    data = None
    status_code = getattr(response, "status_code", 500)

    if isinstance(exc, (InvalidToken, TokenError)):
        message = "El token dado no es válido para ningún tipo de token."
        data = {
            "code": "token_not_valid",
            "messages": exc.args[0].get("messages", [])
            if isinstance(exc.args[0], dict) else []
        }
        status_code = status.HTTP_401_UNAUTHORIZED

    elif isinstance(exc, (AuthenticationFailed, NotAuthenticated)):
        message = "No se proporcionaron credenciales de autenticación o no son válidas."
        data = {"code": "authentication_error"}
        status_code = status.HTTP_401_UNAUTHORIZED

    elif isinstance(exc, ValidationError):
        message = "Error de validación."
        data = {"errors": exc.detail}
        status_code = status.HTTP_400_BAD_REQUEST

    elif isinstance(exc, Http404):
        message = "El recurso solicitado no existe."
        data = None
        status_code = status.HTTP_404_NOT_FOUND

    elif isinstance(exc, PermissionDenied):
        message = "No tienes permisos para realizar esta acción."
        data = None
        status_code = status.HTTP_403_FORBIDDEN

    elif response is None:
        # Error inesperado
        message = "Error Interno del Servidor."
        data = {"error": str(exc)}
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    # Devolver siempre con tu formato unificado
    return Response(
        {
            "success": False,
            "message": message,
            "data": data,
        },
        status=status_code,
    )

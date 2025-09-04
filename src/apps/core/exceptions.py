# core/exceptions.py
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated, ValidationError
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

def custom_exception_handler(exc, context):
    # Obtener la respuesta original
    response = exception_handler(exc, context)
    # Determinar mensaje y data
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
    elif isinstance(exc, (AuthenticationFailed, NotAuthenticated)):
        message = "No se proporcionaron credenciales de autenticación o no son válidas."
        data = {"code": "authentication_error"}
    elif isinstance(exc, ValidationError):
        message = "Error de validación."
        data = {"errors": exc.detail}
    elif response is None:
        # Error inesperado
        message = "Error Interno del Servidor."
        data = {"error": str(exc)}
    # Devolver respuesta con tu formato
    return Response({
        "success": False,
        "message": message,
        "data": data
    }, status=status_code)

# Python
from datetime import timedelta
# Django
from django.conf import settings
from django.utils.timezone import now

def set_jwt_cookies(response, access_token, refresh_token):
    # Configuración general para cookies seguras
    cookie_settings = {
        'httponly': True,                    # No accesible desde JavaScript (mitiga XSS)
        'secure': not settings.DEBUG,       # Solo sobre HTTPS en producción
        'samesite': 'Lax',                  # Previene CSRF en la mayoría de casos
    }
    # Establecer el token de acceso (corta duración)
    response.set_cookie(
        key='access_token',
        value=str(access_token),
        expires=now() + timedelta(hours=24),  # o usa access_token.access_token.payload['exp']
        **cookie_settings
    )
    # Establecer el token de refresh (larga duración)
    response.set_cookie(
        key='refresh_token',
        value=str(refresh_token),
        expires=now() + timedelta(days=7),
        **cookie_settings
    )
    return response
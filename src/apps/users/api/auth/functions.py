# Python
from datetime import datetime, timezone
# Django
from django.middleware.csrf import get_token
# Simple JWT
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken, OutstandingToken, BlacklistedToken
from rest_framework_simplejwt.exceptions import TokenError
# Django
from django.conf import settings
# Para Produccion
'''
def set_jwt_cookies(response, access_token, refresh_token, request=None, domain=None):
    if settings.DEBUG:
        return response  # En local no usamos cookies

    cookie_settings = {
        "httponly": True,
        "secure": True,       # Solo HTTPS
        "samesite": "None",   # Necesario para cross-domain
        "path": "/",
    }

    access_obj = AccessToken(access_token)
    refresh_obj = RefreshToken(refresh_token)

    response.set_cookie(
        "access_token",
        str(access_token),
        expires=datetime.fromtimestamp(access_obj["exp"]),
        **cookie_settings
    )
    response.set_cookie(
        "refresh_token",
        str(refresh_token),
        expires=datetime.fromtimestamp(refresh_obj["exp"]),
        **cookie_settings
    )

    if request:
        response.set_cookie(
            "csrftoken",
            get_token(request),
            httponly=False,
            secure=True,
            samesite="None",
            path="/"
        )

    return response
'''

def set_jwt_cookies(response, access_token, refresh_token, request=None, domain=None):
    """
    Establece cookies JWT y CSRF token según el entorno.
    """
    domain = domain or getattr(settings, "FRONTEND_DOMAIN", "")

    if not settings.DEBUG:
        return response

    is_local = domain.startswith("http://localhost") or domain.startswith("http://127.0.0.1")

    cookie_settings = {
        "httponly": True,
        "secure": not is_local,
        "samesite": "Lax" if is_local else "None",
        "path": "/",
    }

    access_obj = AccessToken(access_token)
    refresh_obj = RefreshToken(refresh_token)

    for token_name, token_obj in [("access_token", access_obj), ("refresh_token", refresh_obj)]:
        response.set_cookie(
            token_name,
            str(token_obj),
            max_age=int(token_obj["exp"] - datetime.now(timezone.utc).timestamp()),
            domain=None if is_local else domain,
            **cookie_settings
        )

    if request:
        response.set_cookie(
            "csrftoken",
            get_token(request),
            httponly=False,
            secure=cookie_settings["secure"],
            samesite=cookie_settings["samesite"],
            domain=None if is_local else domain,
            path="/"
        )

    return response


def create_new_refresh_token(user, single_session=True):
    if single_session:
        now = datetime.now(timezone.utc)
        active_tokens = OutstandingToken.objects.filter(user=user, expires_at__gt=now)
        for token in active_tokens:
            if not BlacklistedToken.objects.filter(token=token).exists():
                BlacklistedToken.objects.create(token=token)

    refresh = RefreshToken.for_user(user)
    access = refresh.access_token

    access["id"] = str(user.id)
    access["email"] = user.email
    access["email_verified"] = getattr(user, "email_verified", False)

    return refresh, access


def validate_refresh_token(refresh_token_str: str) -> RefreshToken:
    """
    Valida que el refresh token:
    - Sea válido.
    - No esté expirado.
    - No esté en blacklist.
    Devuelve el objeto RefreshToken si todo está OK.
    """
    try:
        refresh = RefreshToken(refresh_token_str)
        refresh.check_blacklist()
    except TokenError as e:
        raise TokenError(f"Refresh token inválido: {str(e)}")
    return refresh


# ------------------------------
# Limpieza de tokens viejos
# ------------------------------
def cleanup_outstanding_tokens():
    """Elimina OutstandingToken que ya expiraron."""
    now = datetime.now(timezone.utc)
    expired_tokens = OutstandingToken.objects.filter(expires_at__lt=now)
    count, _ = expired_tokens.delete()
    return count


def cleanup_blacklisted_tokens():
    """
    Elimina entradas en BlacklistedToken que corresponden a OutstandingToken ya expirados.
    """
    now = datetime.now(timezone.utc)
    expired_outstanding_ids = OutstandingToken.objects.filter(expires_at__lt=now).values_list("id", flat=True)
    count, _ = BlacklistedToken.objects.filter(token_id__in=expired_outstanding_ids).delete()
    return count
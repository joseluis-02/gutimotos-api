import json
from pathlib import Path
from datetime import timedelta

from django.core.exceptions import ImproperlyConfigured

import firebase_admin
from firebase_admin import credentials

from .base import *

APP_DIR = Path(BASE_DIR)

# /var/www/gutimotos/prod
PROJECT_ROOT = APP_DIR.parent.parent.parent

SECRETS_DIR = PROJECT_ROOT / "secrets"
STATIC_DIR = PROJECT_ROOT / "static"

# SECRET.JSON
with open(SECRETS_DIR / "secret.json", encoding="utf-8") as f:
    secret = json.load(f)


def get_env_variable(name, secrets=secret):
    value = secrets.get(name)

    if value is None:
        raise ImproperlyConfigured(
            f"La variable '{name}' no existe en secret.json"
        )

    return value

# DJANGO
SECRET_KEY = get_env_variable("SECRET_KEY")

DEBUG = False

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
]

ALLOWED_HOSTS += get_env_variable("ALLOWED_HOSTS")

# CORS / CSRF
FRONTEND_DOMAINS = get_env_variable("FRONTEND_DOMAINS")

CORS_ALLOWED_ORIGINS = FRONTEND_DOMAINS
CSRF_TRUSTED_ORIGINS = FRONTEND_DOMAINS

CORS_ALLOW_CREDENTIALS = True

# BASE DE DATOS
DATABASES = {
    "default": {
        "ENGINE": get_env_variable("DB_ENGINE"),
        "NAME": get_env_variable("DB_NAME"),
        "USER": get_env_variable("DB_USER"),
        "PASSWORD": get_env_variable("DB_PASSWORD"),
        "HOST": get_env_variable("DB_HOST"),
        "PORT": get_env_variable("DB_PORT"),
        "OPTIONS": {
            "sslmode": "require",
            "connect_timeout": 10,
        },
    }
}

# DJANGO Q
Q_CLUSTER = {
    "name": "gutimotos",
    "workers": 1,
    "recycle": 300,
    "timeout": 60,
    "retry": 90,
    "max_attempts": 3,
    "compress": True,
    "save_limit": 50,
    "queue_limit": 100,
    "ack_failures": True,
    "label": "Django Q",
    "redis": {
        "host": get_env_variable("REDIS_HOST"),
        "port": int(get_env_variable("REDIS_PORT")),
        "db": int(get_env_variable("REDIS_DB")),
        "password": get_env_variable("REDIS_PASSWORD"),
        "socket_timeout": 5,
    },
}

# AWS S3
AWS_ACCESS_KEY_ID = get_env_variable("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = get_env_variable("AWS_SECRET_ACCESS_KEY")

AWS_STORAGE_BUCKET_NAME = get_env_variable(
    "AWS_STORAGE_BUCKET_NAME"
)

AWS_S3_REGION_NAME = get_env_variable(
    "AWS_S3_REGION_NAME"
)

AWS_S3_CUSTOM_DOMAIN = (
    f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"
)

AWS_QUERYSTRING_AUTH = False
AWS_DEFAULT_ACL = None
AWS_S3_FILE_OVERWRITE = False

AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl": "max-age=31536000",
}

# STORAGE DJANGO 5+
STORAGES = {
    "default": {
        "BACKEND": (
            "storages.backends.s3boto3.S3Boto3Storage"
        ),
        "OPTIONS": {
            "bucket_name": AWS_STORAGE_BUCKET_NAME,
            "location": "media",
        },
    },
    "staticfiles": {
        "BACKEND": (
            "whitenoise.storage."
            "CompressedManifestStaticFilesStorage"
        ),
    },
}

# STATIC FILES
STATIC_URL = "/static/"

STATIC_ROOT = STATIC_DIR

STATICFILES_DIRS = [
    APP_DIR / "static",
]

# MEDIA FILES
MEDIA_URL = (
    f"https://{AWS_S3_CUSTOM_DOMAIN}/media/"
)

# DJANGO REST FRAMEWORK
REST_FRAMEWORK = {
    "COERCE_DECIMAL_TO_STRING": True,
    "EXCEPTION_HANDLER":
        "apps.core.exceptions.custom_exception_handler",
}

# FIREBASE
if not firebase_admin._apps:
    cred = credentials.Certificate(
        SECRETS_DIR / "firebase-admin-key.json"
    )

    firebase_admin.initialize_app(cred)

# JWT
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME":
        timedelta(minutes=30),

    "REFRESH_TOKEN_LIFETIME":
        timedelta(days=7),

    "ROTATE_REFRESH_TOKENS": True,

    "BLACKLIST_AFTER_ROTATION": True,

    "UPDATE_LAST_LOGIN": True,

    "SIGNING_KEY": SECRET_KEY,

    "AUTH_HEADER_TYPES": ("Bearer",),
}

# AMAZON SES
EMAIL_BACKEND = (
    "anymail.backends.amazon_ses.EmailBackend"
)

ANYMAIL = {
    "AMAZON_SES_CLIENT_PARAMS": {
        "region_name":
            get_env_variable("AWS_SES_REGION_NAME"),

        "aws_access_key_id":
            AWS_ACCESS_KEY_ID,

        "aws_secret_access_key":
            AWS_SECRET_ACCESS_KEY,
    }
}

DEFAULT_FROM_EMAIL = get_env_variable(
    "DEFAULT_FROM_EMAIL"
)

SERVER_EMAIL = get_env_variable(
    "SERVER_EMAIL"
)

# INTERNACIONALIZACIÓN
LANGUAGE_CODE = "es-BO"

TIME_ZONE = "America/La_Paz"

USE_I18N = True

USE_TZ = True

# SEGURIDAD
SECURE_SSL_REDIRECT = True

SESSION_COOKIE_SECURE = True

CSRF_COOKIE_SECURE = True

SECURE_CONTENT_TYPE_NOSNIFF = True

X_FRAME_OPTIONS = "DENY"

SECURE_PROXY_SSL_HEADER = (
    "HTTP_X_FORWARDED_PROTO",
    "https",
)
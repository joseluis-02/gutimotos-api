# Python
import json
from pathlib import Path
from datetime import timedelta

import firebase_admin
from firebase_admin import credentials
from django.core.exceptions import ImproperlyConfigured

from .base import *

# CORE
DEBUG = False

APP_DIR = Path(BASE_DIR)
PROJECT_ROOT = APP_DIR.parent.parent
SECRETS_DIR = PROJECT_ROOT / "secrets"

# Logs
LOG_DIR = PROJECT_ROOT / "logs" / "django"
LOG_DIR.mkdir(parents=True, exist_ok=True)

# SECRETS LOADER
with open(SECRETS_DIR / "secret.json") as f:
    secret = json.load(f)


def get_env_variable(name):
    try:
        return secret[name]
    except KeyError:
        raise ImproperlyConfigured(f"Missing required secret: {name}")


# HELPERS
def parse_list(value):
    """
    Convierte string JSON o CSV en lista segura.
    """
    if isinstance(value, list):
        return value

    if isinstance(value, str):
        try:
            return json.loads(value)
        except Exception:
            return [v.strip() for v in value.split(",") if v.strip()]

    return []

# SECURITY
SECRET_KEY = get_env_variable("SECRET_KEY")

ALLOWED_HOSTS = parse_list(get_env_variable("ALLOWED_HOSTS"))

FRONTEND_DOMAINS = parse_list(get_env_variable("FRONTEND_DOMAINS"))

# CORS / CSRF
CORS_ALLOWED_ORIGINS = FRONTEND_DOMAINS
CSRF_TRUSTED_ORIGINS = FRONTEND_DOMAINS
CORS_ALLOW_CREDENTIALS = True

# SECURITY HEADERS (PRODUCTION SAFE)
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

SECURE_SSL_REDIRECT = True

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"

# DATABASE
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

# REDIS / Q CLUSTER
Q_CLUSTER = {
    "name": "gutimotos",
    "workers": 1,
    "recycle": 300,
    "timeout": 120,
    "retry": 180,
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
        "socket_connect_timeout": 5,
    }
}

# AWS S3 STORAGE
AWS_ACCESS_KEY_ID = get_env_variable("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = get_env_variable("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = get_env_variable("AWS_STORAGE_BUCKET_NAME")
AWS_S3_REGION_NAME = get_env_variable("AWS_S3_REGION_NAME")

AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"

AWS_QUERYSTRING_AUTH = False
AWS_DEFAULT_ACL = None
AWS_S3_FILE_OVERWRITE = False

AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl": "max-age=31536000",
}

STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
        "OPTIONS": {
            "location": "media",
            "bucket_name": AWS_STORAGE_BUCKET_NAME,
            "custom_domain": AWS_S3_CUSTOM_DOMAIN,
        },
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

STATIC_URL = "/static/"
STATIC_ROOT = PROJECT_ROOT / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]

MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/media/"

# REST FRAMEWORK
REST_FRAMEWORK = {
    "COERCE_DECIMAL_TO_STRING": True,
    "EXCEPTION_HANDLER": "apps.core.exceptions.custom_exception_handler",
}

# FIREBASE (SAFE INIT)
if not firebase_admin._apps:
    cred = credentials.Certificate(SECRETS_DIR / "firebase-admin-key.json")
    firebase_admin.initialize_app(cred)

# JWT
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": True,
    "SIGNING_KEY": SECRET_KEY,
    "AUTH_HEADER_TYPES": ("Bearer",),
}

# EMAIL (SES)
EMAIL_BACKEND = "anymail.backends.amazon_ses.EmailBackend"

ANYMAIL = {
    "AMAZON_SES_CLIENT_PARAMS": {
        "region_name": get_env_variable("AWS_SES_REGION_NAME"),
        "aws_access_key_id": AWS_ACCESS_KEY_ID,
        "aws_secret_access_key": AWS_SECRET_ACCESS_KEY,
    }
}

DEFAULT_FROM_EMAIL = get_env_variable("DEFAULT_FROM_EMAIL")
SERVER_EMAIL = get_env_variable("SERVER_EMAIL")

# I18N / TIMEZONE
LANGUAGE_CODE = "es-BO"
TIME_ZONE = "America/La_Paz"

USE_I18N = True
USE_TZ = True

# LOGGING (ROBUSTO)
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{asctime} {levelname} {name} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "file": {
            "level": "WARNING",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOG_DIR / "django.log",
            "maxBytes": 10 * 1024 * 1024,
            "backupCount": 5,
            "formatter": "verbose",
        },
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["file", "console"],
        "level": "WARNING",
    },
    "loggers": {
        "django": {
            "handlers": ["file"],
            "level": "WARNING",
            "propagate": False,
        },
    },
}
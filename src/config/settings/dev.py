import os
import json
from datetime import timedelta
from .base import *
import firebase_admin
from firebase_admin import credentials

# === Función para leer listas desde variables de entorno ===
def get_env_list(var_name, default=None, sep=','):
    value = os.environ.get(var_name)
    if value:
        return [item.strip() for item in value.split(sep) if item.strip()]
    return default if default is not None else []

# === Secretos y modo debug ===
SECRET_KEY = os.environ.get('SECRET_KEY')
DEBUG = False

# === Hosts y Frontend Domains ===
ALLOWED_HOSTS = ["127.0.0.1", "localhost"] + get_env_list("ALLOWED_HOSTS", default=[])
FRONTEND_DOMAINS = get_env_list("FRONTEND_DOMAINS", default=[])

# CSRF y CORS
CSRF_TRUSTED_ORIGINS = FRONTEND_DOMAINS
CORS_ALLOWED_ORIGINS = FRONTEND_DOMAINS
CORS_ALLOW_CREDENTIALS = True

# === Database ===
DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DB_ENGINE'),
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT'),
        'OPTIONS': {
            'sslmode': 'require',
            'channel_binding': 'require',
        },
    }
}

# === AWS S3 ===
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME")
AWS_S3_REGION_NAME = os.environ.get("AWS_S3_REGION_NAME")
AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"

AWS_QUERYSTRING_AUTH = False
AWS_DEFAULT_ACL = None
AWS_S3_FILE_OVERWRITE = False
AWS_S3_OBJECT_PARAMETERS = {"CacheControl": "max-age=31536000"}

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

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]
MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/media/"

# === Django REST Framework ===
REST_FRAMEWORK = {
    'COERCE_DECIMAL_TO_STRING': True,
    'EXCEPTION_HANDLER': 'apps.core.exceptions.custom_exception_handler',
}

# === Firebase ===
firebase_key_json = os.environ.get("FIREBASE_KEY_JSON")
if firebase_key_json:
    cred_dict = json.loads(firebase_key_json)
    cred = credentials.Certificate(cred_dict)
    firebase_admin.initialize_app(cred)

# === JWT ===
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": True,
    "SIGNING_KEY": SECRET_KEY,
    "AUTH_HEADER_TYPES": ("Bearer",),
}

# === Localización e internacionalización ===
LANGUAGE_CODE = 'es-BO'
TIME_ZONE = 'America/La_Paz'
USE_I18N = True
USE_L10N = True
USE_TZ = True

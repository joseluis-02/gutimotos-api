#import Python
import os
from datetime import timedelta
# Archivo de configuración base
from .base import *
# Firebase
import firebase_admin
from firebase_admin import credentials

# Leer el archivo de secret de variables de entorno
with open(BASE_DIR / 'secrets' / 'secret.json') as f:
    secret = json.loads(f.read())

def get_env_variable(secret_name, secrets=secret):
    try:
        return secrets[secret_name]
    except KeyError:
        raise ImproperlyConfigured(f"La variable de entorno {secret_name} no está configurada")

# Secret key del proyecto
SECRET_KEY = get_env_variable('SECRET_KEY')

# Modo de depuración
DEBUG = False

# Hosts
ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
]
external_hosts = get_env_variable('ALLOWED_HOSTS')
if external_hosts:
    ALLOWED_HOSTS += external_hosts

# Obtener la lista de dominios desde secret.json
FRONTEND_DOMAINS = get_env_variable("FRONTEND_DOMAINS")
# Validar que siempre sea lista, incluso si está vacía
if not FRONTEND_DOMAINS:
    FRONTEND_DOMAINS = []
# CSRF y CORS
CSRF_TRUSTED_ORIGINS = FRONTEND_DOMAINS
CORS_ALLOWED_ORIGINS = FRONTEND_DOMAINS
CORS_ALLOW_CREDENTIALS = True

# Database
DATABASES = {
    'default': {
        'ENGINE': get_env_variable('DB_ENGINE'),
        'NAME': get_env_variable('DB_NAME'),
        'USER': get_env_variable('DB_USER'),
        'PASSWORD': get_env_variable('DB_PASSWORD'),
        'HOST': get_env_variable('DB_HOST'),
        'PORT': get_env_variable('DB_PORT'),
        'OPTIONS': {
            'sslmode': 'require',
            'channel_binding': 'require',
            'connect_timeout': 10,
        },
    }
}

Q_CLUSTER = {
    'name': 'gutimotos',
    'workers': min(4, os.cpu_count()),
    'recycle': 500,
    'timeout': 90,
    'retry': 120,
    'max_attempts': 3,
    'compress': True,
    'save_limit': 100,
    'queue_limit': 200,
    'ack_failures': True,
    'label': 'Django Q',
    'redis': {
        'host': os.getenv('REDIS_HOST', '127.0.0.1'),
        'port': int(os.getenv('REDIS_PORT', 6379)),
        'db': int(os.getenv('REDIS_DB', 0)),
        'password': os.getenv('REDIS_PASSWORD'),
    }
}

# AWS S3
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

# Usamos el nuevo sistema de almacenamiento recomendado por Django 4.2+
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
# WhiteNoise para STATICFILES
STATIC_URL = '/static/'
STATIC_ROOT = '/var/www/gutimotos/dev/static/'
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# MEDIA
MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/media/"

# Para que DRF no convierta Decimal a float
REST_FRAMEWORK = {
    'COERCE_DECIMAL_TO_STRING': True,  # predeterminado: True
    'EXCEPTION_HANDLER': 'apps.core.exceptions.custom_exception_handler',
}

# Configuración de Firebase
cred = credentials.Certificate(BASE_DIR / 'secrets' / 'firebase-admin-key.json')
firebase_admin.initialize_app(cred)

# SimpleJWT para producción
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": True,
    "SIGNING_KEY": SECRET_KEY,
    "AUTH_HEADER_TYPES": ("Bearer",),
}
# Para que DRF no convierta Decimal a float
REST_FRAMEWORK = {
    'COERCE_DECIMAL_TO_STRING': True,  # predeterminado: True
}

# Idioma de Bolivia
LANGUAGE_CODE = 'es-BO'

# Zona horaria exacta para Bolivia
TIME_ZONE = 'America/La_Paz'
USE_I18N = True      # Habilita la internacionalización
USE_L10N = True      # (opcional, si usas localización por formatos regionales)
USE_TZ = True        # Usa zonas horarias con reconocimiento de tiempo universal (UTC)


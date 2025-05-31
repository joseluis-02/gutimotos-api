#import Python
import os
from datetime import timedelta
# Archivo de configuración base
from .base import *
# Firebase
import firebase_admin
from firebase_admin import credentials

# Leer el archivo de secret de variables de entorno
with open(BASE_DIR/"secret.json") as f:
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
ALLOWED_HOSTS = ["127.0.0.1"]
external_hosts = get_env_variable('ALLOWED_HOSTS')
if external_hosts:
    ALLOWED_HOSTS += external_hosts

# Database
DATABASES = {
    'default': {
        'ENGINE': get_env_variable('DB_ENGINE'),
        'NAME': get_env_variable('DB_NAME'),
        'USER': get_env_variable('DB_USER'),
        'PASSWORD': get_env_variable('DB_PASSWORD'),
        'HOST': get_env_variable('DB_HOST'),
        'PORT': get_env_variable('DB_PORT'),
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

# MEDIA
MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/media/"
# STATIC CONFIG con WhiteNoise y django-compressor
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

'''
# Compressor
THIRD_PARTY_APPS += ('compressor',)

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
]

COMPRESS_ENABLED = not DEBUG
COMPRESS_OFFLINE = True  # Para compresión en producción
'''

# Configuración de Firebase
cred = credentials.Certificate(BASE_DIR / 'firebase-admin-key.json')
firebase_admin.initialize_app(cred)

# Configuración de SimpleJWT
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    # Este código revoca todos los tokens de un usuario
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    # Django actualiza el campo last_login del modelo User
    'UPDATE_LAST_LOGIN': True,
    
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
    #Este campo le dice a SimpleJWT qué clase de token usar para representar el access token.
    #"AUTH_TOKEN_CLASSES": ("path.to.MyCustomAccessToken",),
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    #Si tienes un serializer personalizado, asegúrate de que esté bien validado.
    'TOKEN_OBTAIN_SERIALIZER': 'users.api.auth.serializers.custom_token_obtain_pair.CustomTokenObtainPairSerializer',
}

# Para que DRF no convierta Decimal a float
REST_FRAMEWORK = {
    'COERCE_DECIMAL_TO_STRING': True,  # predeterminado: True
}

'''
# Configuración de django-cors-headers
THIRD_PARTY_APPS += ("corsheaders",)
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    *MIDDLEWARE,
]
CORS_ALLOW_ALL_ORIGINS = DEBUG

# En producción (más seguro):
CORS_ALLOWED_ORIGINS = [
    "https://gutimotos.com",
]
'''

'''
# Asegúrate de que Django redireccione a HTTPS
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
'''
# Idioma de Bolivia
LANGUAGE_CODE = 'es-BO'

# Zona horaria exacta para Bolivia
TIME_ZONE = 'America/La_Paz'
USE_I18N = True      # Habilita la internacionalización
USE_L10N = True      # (opcional, si usas localización por formatos regionales)
USE_TZ = True        # Usa zonas horarias con reconocimiento de tiempo universal (UTC)
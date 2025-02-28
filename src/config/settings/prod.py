# Archivo base de configuración
import os
#import os
from .base import *
# Configuracion de Render
DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1']
# Configuracion de Render
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME','localhost')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)
# Database
DATABASES = {
    'default': {
        'ENGINE': config('DB_ENGINE', default='django.db.backends.sqlite3'),
        'NAME': config('DB_NAME', default='db.sqlite3'),
        'USER': config('DB_USER', default=''),
        'PASSWORD': config('DB_PASSWORD', default=''),
        'HOST': config('DB_HOST', default=''),
        'PORT': config('DB_PORT', default=''),
    }
}

# STATIC FILE
STATICFILES_DIRS = [BASE_DIR / 'static']
# Configura tus credenciales de AWS
AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
# URL base para los archivos
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
AWS_S3_CUSTOM_DOMAIN = False

# URL base para los archivos
STORAGES = {
    # Media
    "default": {
        "BACKEND": "core.aws.s3.MediaStorage",
        #"BACKEND": "storages.backends.s3boto3.S3StaticStorage",
    },
    # CSS JS
    "staticfiles": {
        "BACKEND": "core.aws.s3.StaticStorage",
    },
}

# Ajusta también las URLs para acceder a los archivos en S3:
STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/'
MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'

# Internationalization y configuracion de zona horario
LANGUAGE_CODE = 'es-BO'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True
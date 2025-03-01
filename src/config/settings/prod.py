# Archivo base de configuración
import os
#import os
from .base import *
# Función para obtener las variables de entorno
def get_env_variable(var_name):
    try:
        return os.environ[var_name]
    except KeyError:
        raise ImproperlyConfigured(f"La variable de entorno {var_name} no está configurada")
# Secret key del proyecto
SECRET_KEY = get_env_variable('SECRET_KEY')
# Configuracion de Render
DEBUG = False

ALLOWED_HOSTS = ['216.24.57.1']
# Configuracion de Render

RENDER_EXTERNAL_HOSTNAME = get_env_variable('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': get_env_variable('DB_NAME'),
        'USER': get_env_variable('DB_USER'),
        'PASSWORD': get_env_variable('DB_PASSWORD'),
        'HOST': get_env_variable('DB_HOST'),
        'PORT': get_env_variable('DB_PORT'),
    }
}

# STATIC FILE
# Configura tus credenciales de AWS
AWS_ACCESS_KEY_ID = get_env_variable('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = get_env_variable('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = get_env_variable('AWS_STORAGE_BUCKET_NAME')
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
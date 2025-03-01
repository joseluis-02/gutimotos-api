# Configuración base
from .base import *
# Lectura de mi archivo secreto
with open(BASE_DIR/ "secret.json") as f:
    secret = json.loads(f.read())
    
# Función para obtener las variables de mi archivo secreto
def get_secret(secret_name, secrets=secret):
    try:
        return secrets[secret_name]
    except:
        msg = "la variable %s no existe" % secret_name
        raise ImproperlyConfigured(msg)

# Modo de depuración del proyecto
DEBUG = False
ALLOWED_HOSTS = get_secret('ALLOWED_HOSTS')
SECRET_KEY = get_secret('SECRET_KEY')

# Base de datos
DATABASES = {
    'default': {
        'ENGINE': get_secret('DB_ENGINE'),
        'NAME': get_secret('DB_NAME'),
        'USER': get_secret('DB_USER'),
        'PASSWORD': get_secret('DB_PASSWORD'),
        'HOST': get_secret('DB_HOST'),
        'PORT': get_secret('DB_PORT'),
    }
}

# STATIC FILE
# Configura tus credenciales de AWS
AWS_ACCESS_KEY_ID = get_secret('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = get_secret('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = get_secret('AWS_STORAGE_BUCKET_NAME')
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
# https://docs.djangoproject.com/en/5.1/topics/i18n/
LANGUAGE_CODE = 'es-BO'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True
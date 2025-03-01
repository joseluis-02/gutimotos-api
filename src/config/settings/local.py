# Decouple para obtener las variables de entorno
from decouple import config
# Base configuración base
from .base import *
# Modo de depuración del proyecto
DEBUG = True
SECRET_KEY = config('SECRET_KEY')
ALLOWED_HOSTS = ['127.0.0.1']
# Base de datos
DATABASES = {
    'default': {
        'ENGINE': config('DB_ENGINE'),
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
    }
}

# Configuración de archivos estáticos del proyecto
STATIC_URL = 'static/'
# Configuración de archivos media del proyecto
MEDIA_URL = '/media/'  # URL para acceder a los archivos media
MEDIA_ROOT = BASE_DIR / 'media'# Ruta donde se guardarán los archivos

# Configuración de correo

# Internationalization y configuracion de zona horario
# https://docs.djangoproject.com/en/5.1/topics/i18n/
LANGUAGE_CODE = 'es-BO'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True
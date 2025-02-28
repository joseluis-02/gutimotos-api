# Base configuración base
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
DEBUG = get_secret('DEBUG')
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
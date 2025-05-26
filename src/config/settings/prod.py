#import Python
import os
from datetime import timedelta
# Archivo de configuración base
from .base import *
# Firebase
import firebase_admin
from firebase_admin import credentials

# Función para obtener las variables de entorno
def get_env_variable(var_name):
    try:
        return os.environ[var_name]
    except KeyError:
        raise ImproperlyConfigured(f"La variable de entorno {var_name} no está configurada")
# Secret key del proyecto
SECRET_KEY = get_env_variable('SECRET_KEY')

# Modo de despliegue en developer
DEBUG = False

ALLOWED_HOSTS = ['192.168.1.50']
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

# Configuración de archivos estáticos del proyecto
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / "static",
    # Otros directorios si es necesario
]
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Configuración de archivos media del proyecto
MEDIA_URL = '/media/'  # URL para acceder a los archivos media
MEDIA_ROOT = BASE_DIR / 'media'# Ruta donde se guardarán los archivos

# Busca el path ruta en tu máquina puede variar la ruta
#NPM_BIN_PATH = '/home/usuario/.nvm/versions/node/v22.12.0/bin/npm'

# Configuracion de Compress
COMPRESS_ROOT = BASE_DIR / 'static'
#COMPRESS_ENABLED = True
#STATICFILES_FINDERS = ('compressor.finders.CompressorFinder',)

# Configuración de Firebase
cred = credentials.Certificate(BASE_DIR / 'firebase-admin-key.json')
firebase_admin.initialize_app(cred)
# Configuración de SimpleJWT
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(minutes=10),
    # Este código revoca todos los tokens de un usuario
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    # Django actualiza el campo last_login del modelo User
    'UPDATE_LAST_LOGIN': True,
    
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    'TOKEN_OBTAIN_SERIALIZER': 'users.api.auth.serializers.custom_token_obtain_pair.CustomTokenObtainPairSerializer',
}

# Para que DRF no convierta Decimal a float
REST_FRAMEWORK = {
    'COERCE_DECIMAL_TO_STRING': True,  # predeterminado: True
}

# Configuración de CORS
# En desarrollo, permite todo
CORS_ALLOW_ALL_ORIGINS = DEBUG

# Internationalization y configuracion de zona horario
LANGUAGE_CODE = 'es-BO'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True
# Python
from datetime import timedelta
# Firebase
import firebase_admin
from firebase_admin import credentials, auth
# Decouple para obtener las variables de entorno
from decouple import config
# Base configuración base
from .base import *
# Modo de depuración del proyecto
DEBUG = True
SECRET_KEY = config('SECRET_KEY')
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]
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
# Apps de terceros
THIRD_PARTY_APPS_LOCAL = (
    'django_browser_reload',
)
INSTALLED_APPS = INSTALLED_APPS + THIRD_PARTY_APPS_LOCAL
# Middleware solo para desarrollo
MIDDLEWARE.append('django_browser_reload.middleware.BrowserReloadMiddleware')

# Configuración de CORS y CSRF para desarrollo
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8000",  # Frontend React local
    "http://127.0.0.1:8000",
]
CORS_ALLOW_CREDENTIALS = True

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]
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
cred = credentials.Certificate(BASE_DIR / 'secrets/firebase-admin-key.json')
firebase_admin.initialize_app(cred)
# JWT local
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "SIGNING_KEY": SECRET_KEY,
    "AUTH_HEADER_TYPES": ("Bearer",),
}

# Para que DRF no convierta Decimal a float
REST_FRAMEWORK = {
    'COERCE_DECIMAL_TO_STRING': True,  # predeterminado: True
}

# Configuración de CORS
# En desarrollo, permite todo
CORS_ALLOW_ALL_ORIGINS = DEBUG

# En producción, especifica los dominios permitidos
'''
CORS_ALLOWED_ORIGINS = [
    "https://tudominio.com",
    "https://admin.tudominio.com",
]
'''
# Solo en producción permite el uso de cookies, cabeceras de autorización, sesiones entre el frontend y el backend.
# CORS_ALLOW_CREDENTIALS = True

# Configuración de CSRF y cookies Solo en producción
# CSRF_COOKIE_SECURE = True
# SESSION_COOKIE_SECURE = True

# Configuración de correo

# Internationalization y configuracion de zona horario
# https://docs.djangoproject.com/en/5.1/topics/i18n/
LANGUAGE_CODE = 'es-BO'

TIME_ZONE = 'America/La_Paz'

USE_I18N = True

USE_TZ = True
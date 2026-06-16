# Python
from datetime import timedelta
# Firebase
import firebase_admin
from firebase_admin import credentials, auth
# Decouple para obtener las variables de entorno
from decouple import config
# Base configuración base
from .base import *

# Leer secrets
with open(BASE_DIR / "secrets" / "secret.json") as f:
    secrets = json.load(f)

def get_env_variable(secret_name):
    try:
        value = secrets[secret_name]
        if isinstance(value, str):
            return value.strip()  # elimina espacios invisibles
        return value
    except KeyError:
        from django.core.exceptions import ImproperlyConfigured
        raise ImproperlyConfigured(f"La variable de entorno {secret_name} no está configurada")

# Modo de depuración del proyecto
DEBUG = True
SECRET_KEY = get_env_variable('SECRET_KEY')
ALLOWED_HOSTS = ["127.0.0.1","*"]
# Base de datos
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

# Apps de terceros
THIRD_PARTY_APPS_LOCAL = (
    'django_browser_reload',
)
INSTALLED_APPS = INSTALLED_APPS + THIRD_PARTY_APPS_LOCAL
# Middleware solo para desarrollo
MIDDLEWARE.append('django_browser_reload.middleware.BrowserReloadMiddleware')
# Configuración de CORS
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

# En desarrollo, permite todo
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "https://*.ngrok-free.app",
]
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False


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

# Configuración de Twilio
TWILIO_ACCOUNT_SID=get_env_variable('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN=get_env_variable('TWILIO_AUTH_TOKEN')
TWILIO_WHATSAPP_NUMBER=get_env_variable('TWILIO_WHATSAPP_NUMBER')


# PHONENUMBER
PHONENUMBER_DEFAULT_REGION = None
PHONENUMBER_DEFAULT_FORMAT = "E164"

# CELERY

# Configuración principal de Django Q
Q_CLUSTER = {
    'name': 'gutimotos-dev',
    'workers': 2,              # Pocos workers para desarrollo
    'recycle': 100,            # Reciclar más seguido
    'timeout': 30,             # Timeout corto para detectar problemas
    'compress': False,         # No comprimir (más fácil debug)
    'save_limit': 50,          # Mantener menos registros
    'queue_limit': 100,        # Cola pequeña
    'cpu_affinity': 1,
    'label': 'Django Q Dev',
    'redis': {
        'host': '127.0.0.1',
        'port': 6379,
        'db': 0,
    }
}

EMAIL_BACKEND = "anymail.backends.amazon_ses.EmailBackend"
# Configuración SES
ANYMAIL = {
    "AMAZON_SES_CLIENT_PARAMS": {
        "region_name": "sa-east-1",
        # "aws_access_key_id": "TU_KEY",
        # "aws_secret_access_key": "TU_SECRET",
    }
}
# Opcional: valores por defecto de Django
DEFAULT_FROM_EMAIL = get_env_variable("DEFAULT_FROM_EMAIL")
SERVER_EMAIL = get_env_variable("SERVER_EMAIL")

# Internationalization y configuracion de zona horario
# https://docs.djangoproject.com/en/5.1/topics/i18n/
LANGUAGE_CODE = 'es-BO'
TIME_ZONE = 'America/La_Paz'
USE_I18N = True
USE_TZ = True
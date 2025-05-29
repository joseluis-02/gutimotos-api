# Python
import os
import json
# Pathlib
from pathlib import Path
# Django
from django.core.exceptions import ImproperlyConfigured

# Obtenemos base del proyecto es decir la carpeta raíz.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Aplicaciones de django 
DJANGO_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)
# Aplicaciones de terceros creados por otros desarrolladores
THIRD_PARTY_APPS = (
    # Aquí define aplicaciones de otros desarrolladores
    'rest_framework',
    # Simple JWT
    'rest_framework_simplejwt.token_blacklist',
    # Storage de archivos
    'storages',
    # Filters
    'django_filters',
    # Htmx
    "django_htmx",
)
# Aplicaciones locales o creados por ti
LOCAL_APPS = (
    # Aquí instala tus aplicaciones
    'apps.core',
    'apps.persons',
    'apps.categories',
    'apps.measures',
    'apps.prices',
    'apps.products',
    'apps.motorcycles',
    'apps.users',
)

# Definición general de aplicaciones
INSTALLED_APPS = DJANGO_APPS+THIRD_PARTY_APPS+LOCAL_APPS

# Middlewares del proyecto
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # WhiteNoise middleware
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Middleware para el manejo de HTMX
    "django_htmx.middleware.HtmxMiddleware",
]
# Backends de la API
REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend'
    ],
}
# Archivo root de las urls del proyecto
ROOT_URLCONF = 'config.urls'

# Configuración de la carpeta de templates para trabajar con vistas
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'], # Plantillas globales
        'APP_DIRS': True, # Habilita la búsqueda de templates dentro de las apps
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Definición modo de ejecución del proyecto
WSGI_APPLICATION = 'config.wsgi.application'

# Password validaciones de la contraseña en proyecto
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
# Uso de User Personalizado
AUTH_USER_MODEL = 'users.User'

# Definición del tamaño del id auto_increment para todos lo modelos dentro del proyecto
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
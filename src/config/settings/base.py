from pathlib import Path

# Decouple 
from decouple import config, Csv

# Obtenemos base del proyecto es decir la carpeta raíz.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Secret key del proyecto
SECRET_KEY = config('SECRET_KEY', default='inseguro')

# Aplicaciones de django 
DJANGO_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)
# Aplicaciones locales o creados por ti
LOCAL_APPS = (
    # Aquí instala tus aplicaciones
)
# Aplicaciones de terceros creados por otros desarrolladores
THIRD_PARTY_APPS = (
    # Aquí define aplicaciones de otros desarrolladores
    'rest_framework',
)
# Definición general de aplicaciones
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# Middlewares del proyecto
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Archivo root de las urls del proyecto
ROOT_URLCONF = 'config.urls'

# Configuración de la carpeta de templates para trabajar con vistas
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
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

# Definición del tamaño del id auto_increment para todos lo modelos dentro del proyecto
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
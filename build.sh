#!/bin/bash
set -e

# Instalar dependencias sin las de desarrollo
poetry install --no-dev
# Configurar el entorno con la versión correcta de Python
poetry env use python3.11
# Migraciones de base de datos (si es necesario)
poetry run python src/manage.py makemigrations
poetry run python src/manage.py migrate

# Recolectar archivos estáticos (si es necesario para producción)
poetry run python src/manage.py collectstatic --noinput

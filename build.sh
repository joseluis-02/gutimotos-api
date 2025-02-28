#!/usr/bin/env bash
# Exit on error
set -o errexit
echo "Entra al bash"
echo "Cargando el proyecto..."
# Instalar Poetry
curl -sSL https://install.python-poetry.org | python3 -

# Asegúrate de que el PATH de Poetry esté configurado correctamente
export PATH="$HOME/.local/bin:$PATH"

# Instalar las dependencias de tu proyecto usando Poetry
poetry install --no-dev

# Migraciones de base de datos (si es necesario)
poetry run python src/manage.py makemigrations
poetry run python src/manage.py migrate

# Recolectar archivos estáticos (si es necesario para producción)
poetry run python src/manage.py collectstatic --noinput

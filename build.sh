#!/usr/bin/env bash
# Exit on error
set -o errexit
echo "Entra al bash"
echo "Cargando el proyecto..."
# Instalar Poetry sin crear un entorno virtual global (usar el entorno actual)
curl -sSL https://install.python-poetry.org | python3 - --no-venv

# Asegurarse de que Poetry esté en el PATH
export PATH="$HOME/.local/bin:$PATH"

# Instalar dependencias del proyecto usando Poetry
poetry install --no-dev

# Migraciones de base de datos (si es necesario)
poetry run python src/manage.py makemigrations
poetry run python src/manage.py migrate

# Recolectar archivos estáticos (si es necesario para producción)
poetry run python src/manage.py collectstatic --noinput

#!/usr/bin/env bash
# Exit on error
set -o errexit
echo "Entra al bash"
echo "Cargando el proyecto..."
# Actualizar el sistema y asegurarse de que pip está actualizado
apt-get update
apt-get install -y python3-pip python3-dev libpq-dev

# Instalar Poetry (si no está instalado)
curl -sSL https://install.python-poetry.org | python3 -

# Agregar Poetry al PATH
export PATH="$HOME/.local/bin:$PATH"

# Instalar las dependencias de Poetry
poetry install

# Migraciones de base de datos (si es necesario)
poetry run python src/manage.py makemigrations
poetry run python src/manage.py migrate

# Recolectar archivos estáticos (si es necesario para producción)
poetry run python src/manage.py collectstatic --noinput

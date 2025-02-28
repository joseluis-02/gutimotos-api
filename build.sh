#!/usr/bin/env bash
# Exit on error
set -o errexit
echo "Entra al bash"
echo "Cargando el proyecto..."
# Hacer que el script falle si algún comando falla
set -e

# Instalar Poetry (si no está ya instalado)
if ! command -v poetry &> /dev/null
then
    echo "Poetry no encontrado, instalando..."
    curl -sSL https://install.python-poetry.org | python3 -
fi

# Agregar Poetry a la PATH
export PATH="$HOME/.poetry/bin:$PATH"

# Configurar el entorno virtual usando Poetry
poetry config virtualenvs.in-project true

# Instalamos las dependencias del proyecto
poetry install --no-dev  # --no-dev omite las dependencias de desarrollo en producción


# Migraciones de base de datos (si es necesario)
poetry run python src/manage.py makemigrations
poetry run python src/manage.py migrate

# Recolectar archivos estáticos (si es necesario para producción)
poetry run python src/manage.py collectstatic --noinput

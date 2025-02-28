#!/bin/bash
set -e

# Verificar si la versión de Python es correcta
python_version=$(python --version)
if [[ $python_version != "Python 3.12"* ]]; then
  echo "La versión de Python es incorrecta. Cambiando a Python 3.12..."
  pyenv install 3.12.0
  pyenv global 3.12.0
fi

# Instalar Poetry si no está instalado
if ! command -v poetry &> /dev/null
then
    echo "Poetry no encontrado, instalando..."
    curl -sSL https://install.python-poetry.org | python3 -
fi

# Agregar Poetry a la PATH
export PATH="$HOME/.poetry/bin:$PATH"

# Configurar el entorno virtual usando Poetry
poetry config virtualenvs.in-project true

# Instalar dependencias sin las de desarrollo
poetry install --no-dev


# Migraciones de base de datos (si es necesario)
poetry run python src/manage.py makemigrations
poetry run python src/manage.py migrate

# Recolectar archivos estáticos (si es necesario para producción)
poetry run python src/manage.py collectstatic --noinput

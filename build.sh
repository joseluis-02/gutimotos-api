#!/bin/bash

# Asegurarse de que Poetry use Python 3.11
poetry env use python3.11 || exit 1

# Instalar dependencias sin las de desarrollo
poetry install --only main || exit 1

ruta_actual=$(pwd)
echo "La ruta actual es: $ruta_actual"
# Moverse al directorio correcto
cd src || exit 1
#cd ..
ls
ruta_actual=$(pwd)
echo "La ruta actual es: $ruta_actual"

# Ejecutar migraciones
poetry run python manage.py makemigrations || exit 1
poetry run python manage.py migrate || exit 1

# Recolectar archivos estáticos (si es necesario)
poetry run python manage.py collectstatic --noinput || exit 1

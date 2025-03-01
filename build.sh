#!/usr/bin/env bash
# Salir si ocurre un error
set -o errexit  

# Especificar la versión de Python (Render usa 3.11 por defecto)
poetry env use 3.11 || echo "Python 3.11 ya está en uso"

# Instalar dependencias
poetry install --no-root --no-interaction
echo "Instalación completada"

# Entrar a src de mi proyecto
cd src || exit 1
# Ejecutar migraciones
poetry run python manage.py makemigrations || exit 1
poetry run python manage.py migrate || exit 1
echo "Migración completada"

# Recolectar archivos estáticos (si es necesario)
poetry run python manage.py collectstatic --noinput || exit 1
echo "Archivo estático recolectado"
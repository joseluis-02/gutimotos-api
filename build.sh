#!/usr/bin/env bash
# Salir si ocurre un error
set -o errexit  

# Especificar la versión de Python (Render usa 3.11 por defecto)
poetry env use 3.11 || echo "Python 3.11 ya está en uso"

# Instalar dependencias
poetry install --no-root --no-interaction

echo "Instalación completada"
# Mostrar la ruta actual
echo "Ruta actual después del ajuste:"
pwd
cd src || exit 1
echo "Ruta actual después de cambiar a src:"
pwd
echo "Directorios:"
ls -la
# Ejecutar migraciones
poetry run python manage.py makemigrations || exit 1
poetry run python manage.py migrate || exit 1

# Recolectar archivos estáticos (si es necesario)
poetry run python manage.py collectstatic --noinput || exit 1

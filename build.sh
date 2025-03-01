#!/usr/bin/env bash
# Salir si ocurre un error
set -o errexit  

# Especificar la versión de Python (Render usa 3.11 por defecto)
poetry env use 3.11 || echo "Python 3.11 ya está en uso"

# Instalar dependencias
poetry install --no-root

# Exportar variables para evitar problemas con `src/src`
export PYTHONPATH=/opt/render/project/src

echo "Instalación completada"
# Mostrar la ruta actual
echo "Ruta actual después del ajuste:"
pwd
# Ejecutar migraciones
#poetry run python manage.py makemigrations || exit 1
#poetry run python manage.py migrate || exit 1

# Recolectar archivos estáticos (si es necesario)
#poetry run python manage.py collectstatic --noinput || exit 1

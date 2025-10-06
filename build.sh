#!/usr/bin/env bash
set -o errexit
set -o pipefail

echo "=== Build iniciado ==="

# Instalar dependencias
echo "Instalando dependencias con Poetry..."
poetry install --no-root --no-interaction
echo "Dependencias instaladas ✅"

# Entrar al directorio del proyecto
cd src || { echo "ERROR: No se pudo acceder al directorio src"; exit 1; }

# Ejecutar migraciones (solo migrate)
echo "Aplicando migraciones..."
poetry run python manage.py migrate --noinput
echo "Migraciones aplicadas ✅"

# Recolectar archivos estáticos
echo "Recolectando archivos estáticos..."
poetry run python manage.py collectstatic --noinput
echo "Archivos estáticos recolectados ✅"

echo "=== Build completado exitosamente ==="

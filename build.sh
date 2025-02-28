#!/bin/bash
echo "Iniciando el proceso de construcción..."
# Instalar las dependencias de producción
poetry install --no-dev
echo "Dependencias instaladas."
# Realizar migraciones de la base de datos
python src/manage.py makemigrations --noinput
python src/manage.py migrate --noinput
echo "Migraciones realizadas."
# Compilar activos estáticos (si aplica)
python src/manage.py collectstatic --noinput

# Otros comandos si es necesario
# Moverse al directorio correcto si Render duplicó "src/"
if [ -d "src" ]; then
  cd src
fi

# Mostrar la ruta actual
echo "Ruta actual después del ajuste:"
pwd
# Listar archivos y directorios en la ruta actual
echo "Contenido del directorio actual:"
ls -la  # Esto te ayudará a ver si el código está en la ruta correcta

# Forzar el uso de Python 3.11 en Poetry
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

#!/bin/bash
set -e

echo "Waiting for PostgreSQL to be ready at ${DB_HOST:-db}:${DB_PORT:-5432}..."
until nc -z "${DB_HOST:-db}" "${DB_PORT:-5432}"; do
  echo "PostgreSQL is still starting up..."
  sleep 2
done
echo "PostgreSQL is up!"

echo "Running Django migrations..."
python statuspage/manage.py migrate

echo "Collecting static files..."
python statuspage/manage.py collectstatic --noinput

if [ "$CREATE_SUPERUSER" = "true" ]; then
  echo "Creating superuser if it doesn't exist..."
  python statuspage/manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', '', 'adminpassword')
EOF
fi

echo "Starting Gunicorn..."
exec gunicorn statuspage.wsgi:application --bind 0.0.0.0:8000
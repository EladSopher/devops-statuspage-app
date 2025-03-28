#!/bin/bash

set -euxo pipefail  # Exit on error, treat unset vars as errors, and fail on pipes

echo "==> DATABASE_URL is: $DATABASE_URL"

# Extract DB Host and Port from DATABASE_URL
DB_HOST=$(echo "$DATABASE_URL" | sed -E 's|.@([^:/]+):([0-9]+).|\1|')
DB_PORT=$(echo "$DATABASE_URL" | sed -E 's|.@([^:/]+):([0-9]+).|\2|')

echo "Waiting for PostgreSQL to be ready at ${DB_HOST}:${DB_PORT}..."
until nc -z "$DB_HOST" "$DB_PORT"; do
  echo "PostgreSQL is still starting up..."
  sleep 2
done
echo "✅ PostgreSQL is up!"

# Run Django migrations
echo "Running Django migrations..."
python manage.py migrate || { echo "❌ Django migrations failed"; exit 1; }
echo "✅ Migrations completed successfully"

# Collect static files
echo "Collecting static files..."
if ! python manage.py collectstatic --noinput; then
  echo "❌ collectstatic failed — check STATICFILES_DIRS, permissions, or settings"
  exit 1
fi
echo "✅ Static files collected successfully"

# Create superuser if needed
if [ "${CREATE_SUPERUSER:-false}" = "true" ]; then
  echo "Creating superuser if it doesn't exist..."
  python manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', '', 'adminpassword')
    print("✅ Superuser created successfully")
else:
    print("ℹ Superuser already exists")
EOF
  echo "✅ Superuser creation script finished"
else
  echo "ℹ CREATE_SUPERUSER is not set to 'true', skipping superuser creation"
fi

# Check if Gunicorn is installed
if ! command -v gunicorn &>/dev/null; then
  echo "❌ Gunicorn is not installed. Please install it using: pip install gunicorn"
  exit 1
fi

# Start Gunicorn
echo "🟢 Reached Gunicorn startup line"
exec gunicorn statuspage.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --access-logfile - \
    --error-logfile - || { echo "❌ Gunicorn failed to start"; exit 1; }

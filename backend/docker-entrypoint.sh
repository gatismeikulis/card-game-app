#!/bin/bash

set -e  # exit immediately on error

echo "Running database migrations..."
uv run python manage.py migrate

echo "Collecting static files..."
uv run python manage.py collectstatic --noinput

# Create superuser only if environment variables are set and user does not already exist
if [ -n "$SUPERUSER_USERNAME" ] && [ -n "$SUPERUSER_PASSWORD" ]; then
    uv run python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
print('Attempting to create superuser: $SUPERUSER_USERNAME...')
if not User.objects.filter(username='$SUPERUSER_USERNAME').exists():
    User.objects.create_superuser('$SUPERUSER_USERNAME', '${SUPERUSER_EMAIL:-}', '$SUPERUSER_PASSWORD')
    print('Superuser created successfully')
else:
    print('Superuser already exists')
"
else
    echo "Skipping superuser creation - credentials not provided"
fi

echo "Starting server..."

if [ "$ENVIRONMENT" = "production" ]; then
    echo "Running Gunicorn for production..."
    # 3 workers, bind to 0.0.0.0:8000
    exec gunicorn config.wsgi:application \
        --bind 0.0.0.0:8000 \
        --workers 3 \
        --threads 4 \
        --timeout 120
else
    echo "Running Django development server (uv run)..."
    exec uv run python manage.py runserver 0.0.0.0:8000
fi
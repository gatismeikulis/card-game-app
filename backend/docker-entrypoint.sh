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
    echo "Running Daphne for production (ASGI with WebSocket support)..."
    # Single process only - required for InMemoryChannelLayer
    exec uv run daphne -b 0.0.0.0 -p "${PORT}" config.asgi:application
else
    echo "Running Django development server (uv run)..."
    exec uv run python manage.py runserver 0.0.0.0:8000
fi
#!/bin/bash
set -e

# Ожидание готовности базы данных
echo "Waiting for database..."
until alembic current > /dev/null 2>&1; do
  echo "Database is unavailable - sleeping"
  sleep 1
done

echo "Database is up - executing command"

# Применение миграций
echo "Applying migrations..."
alembic upgrade head

# Запуск приложения
echo "Starting application..."
exec "$@"

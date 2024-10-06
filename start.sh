#!/bin/sh

# Ждем, пока база данных будет готова
echo "Waiting for database to be ready..."
while ! nc -z db 5432; do
  sleep 0.1
done
echo "Database is ready!"

# Применяем миграции
echo "Make migrarions"
alembic revision --autogenerate

echo "Applying database migrations..."
alembic upgrade head

# Запускаем приложение
echo "Starting FastAPI application..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
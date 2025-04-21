#!/bin/sh

echo "Ожидание PostgreSQL..."
while ! pg_isready -h "$POSTGRES_HOST" -U "$POSTGRES_USER" -d "$POSTGRES_DB"; do
  echo "⏳ PostgreSQL недоступен — ожидание..."
  sleep 1
done

echo "PostgreSQL готов. Применяем миграции..."
alembic upgrade head

echo "Запуск FastAPI приложения..."
exec uvicorn main:app --host 0.0.0.0 --port 8000
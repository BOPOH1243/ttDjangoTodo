#!/bin/sh
set -e

# Ждём, пока Postgres будет готов
until PGPASSWORD=$POSTGRES_PASSWORD psql -h "$DB_HOST" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c '\q'; do
  echo "Waiting for Postgres…"
  sleep 2
done

# Применяем миграции
echo "Applying database migrations…"
python project/manage.py migrate --noinput

# Собираем статические файлы (если нужно)
# echo "Collecting static files…"
# python project/manage.py collectstatic --noinput

# Запускаем сервер
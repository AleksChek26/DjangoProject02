#!/bin/bash
set -e

# Функция для ожидания готовности БД
wait_for_db() {
    local host="$1"
    local port="$2"
    local max_attempts=30
    local attempt=0

    echo "Waiting for PostgreSQL at $host:$port..."

    while [ $attempt -lt $max_attempts ]; do
        if python -c "
import socket;
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
result = sock.connect_ex(('$host', $port));
sock.close();
exit(result)
" 2>/dev/null; then
            echo "PostgreSQL is ready!"
            return 0
        fi

        attempt=$((attempt + 1))
        echo "Attempt $attempt/$max_attempts: PostgreSQL not ready, waiting 5 seconds..."
        sleep 5
    done

    echo "Error: PostgreSQL not available after $max_attempts attempts"
    exit 1
}

# Функция выполнения миграций БД
run_migrations() {
    echo "Running database migrations..."
    poetry run python manage.py migrate --noinput
    echo "Database migrations completed"
}

# Функция сбора статических файлов
collect_static() {
    if [ "$COLLECT_STATIC" = "true" ] || [ "$DEBUG" = "False" ]; then
        echo "Collecting static files..."
        poetry run python manage.py collectstatic --noinput --clear
        echo "Static files collected"
    fi
}

# Функция создания суперпользователя (опционально)
create_superuser() {
    if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_EMAIL" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
        echo "Creating superuser..."
        python manage.py shell <<EOF
from django.contrib.auth.models import User
if not User.objects.filter(username='$DJANGO_SUPERUSER_USERNAME').exists():
    User.objects.create_superuser(
        username='$DJANGO_SUPERUSER_USERNAME',
        email='$DJANGO_SUPERUSER_EMAIL',
        password='$DJANGO_SUPERUSER_PASSWORD'
    )
    print("Superuser created successfully")
else:
    print("Superuser already exists")
EOF
        echo "Superuser creation completed"
    fi
}

# Основная логика entrypoint
main() {
    # Ожидание готовности БД
    wait_for_db "$DB_HOST" "$DB_PORT"

    # Выполнение миграций
    run_migrations

    # Сбор статических файлов
    collect_static

    # Создание суперпользователя, если заданы переменные окружения
    create_superuser

    # Запуск переданной команды (например, gunicorn или runserver)
    echo "Starting application..."
    exec "$@"
}

# Обработка сигналов для корректного завершения
trap 'echo "Received SIGTERM, shutting down"; exit 0' TERM
trap 'echo "Received SIGINT, shutting down"; exit 0' INT

# Запуск основной логики
main "$@"

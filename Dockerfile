# Этап 1: сборка приложения
FROM python:3.12-slim as builder

WORKDIR /app

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Установка Poetry
RUN pip install poetry

# Копирование файлов зависимостей
COPY pyproject.toml poetry.lock ./

# Установка зависимостей в виртуальное окружение
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

# Этап 2: создание финального образа
FROM python:3.11-slim

WORKDIR /app

# Установка Nginx
RUN apt-get update && apt-get install -y nginx \
    && rm -rf /var/lib/apt/lists/* \
    && rm /etc/nginx/conf.d/default.conf

# Копирование собранного приложения
COPY --from=builder /app /app
COPY --from=builder /root/.cache /root/.cache

# Копирование конфигурации Nginx
COPY nginx.conf /etc/nginx/nginx.conf

# Создание пользователя для приложения
RUN groupadd -r appuser && useradd -r -g appuser appuser
RUN chown -R appuser:appuser /app
RUN chown -R www-data:www-data /var/cache/nginx /var/run/nginx.pid

# Копирование скриптов запуска
COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# Открытие портов
EXPOSE 80

# Точка входа
USER appuser
ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]

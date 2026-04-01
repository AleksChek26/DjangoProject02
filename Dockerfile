# Базовый образ Python
FROM python:3.12-slim

# Устанавливаем зависимости системы
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Рабочая директория
WORKDIR /app

# Копируем и устанавливаем зависимости
COPY pyproject.toml poetry.lock ./
RUN pip install poetry && poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

# Копируем проект
COPY . .

# Открываем порт для Gunicorn
EXPOSE 8000

# Запускаем Gunicorn (можно переопределить в docker-compose)
CMD ["gunicorn", "myproject.wsgi:application", "--bind", "0.0.0.0:8000"]

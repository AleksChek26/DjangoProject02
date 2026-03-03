FROM python:3.12

# Устанавливаем Poetry
RUN pip install poetry

WORKDIR /app

# Копируем файлы зависимостей
COPY pyproject.toml poetry.lock ./

# Устанавливаем зависимости через Poetry
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Копируем код приложения
COPY . .

# Собираем статику (если нужно)
RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0:8000"]

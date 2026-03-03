# Django Project 02 — Онлайн‑платформа обучения
### Многоконтейнерное веб‑приложение на Django REST Framework с использованием Docker Compose.

## Технологии
    Бэкенд: Django + DRF (Django REST Framework);

    База данных: PostgreSQL 15;

    Кэш и брокер сообщений: Redis;

    Фоновые задачи: Celery + Celery Beat;

    Контейнеризация: Docker + Docker Compose;

    Управление зависимостями: Poetry.

## Предварительные требования
### Перед началом работы убедитесь, что у вас установлены:

    Docker Desktop (с поддержкой WSL 2 для Windows);

    Python 3.12+;

    Poetry;

    Git (для клонирования репозитория).

## Установка и запуск
### Шаг 1. Клонирование репозитория

    git clone DjangoProject02

### Шаг 2. Создание файла .env
    Создайте файл .env на основе шаблона:
      .env.example
#### Отредактируйте .env, указав свои значения для чувствительных данных.

###   Шаг 3. Сборка и запуск контейнеров
    Выполните команду для сборки образов и запуска всех сервисов:

    docker-compose up --build
#### Для запуска в фоновом режиме добавьте флаг -d:

    docker-compose up -d --build
### Шаг 4. Выполнение миграций БД
    После запуска контейнеров выполните миграции базы данных:

    docker-compose exec web python manage.py migrate 

### Шаг 5. Создание суперпользователя (опционально)
    Для доступа к админ‑панели Django создайте суперпользователя:

    docker-compose exec web python manage.py createsuperuser

## Проверка работоспособности сервисов
### Веб‑сервис (Django/DRF)
    Откройте в браузере:

     http://localhost:8000
    Должна загрузиться страница Django или интерфейс DRF API.

### База данных (PostgreSQL)

    Проверьте логи сервиса БД:

     docker-compose logs db
    Убедитесь, что нет ошибок подключения.

### Redis

    Проверьте доступность Redis:

     docker-compose exec redis redis-cli ping
    Ожидаемый ответ: PONG.

### Celery (воркер)

    Проверьте логи воркера Celery:

     docker-compose logs celery
    В логах должны быть сообщения о запуске воркера и готовности принимать задачи. 

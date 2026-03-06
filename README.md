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

### Celery Beat (планировщик)
    Проверьте логи планировщика:

     docker-compose logs celery-beat
    В логах должны быть сообщения о планировании периодических задач. Ищите строки вида:

    [INFO] Scheduler: Sending due task <имя_задачи>
    [INFO] DatabaseScheduler: Schedule changed.
    Если планировщик не находит задачи, убедитесь, что: 

     -миграции выполнены(python manage.py migrate)

     -периодические задачи зарегистрированы в admin Django или через код.
 
## Переменные окружения
### Все чувствительные данные вынесены в файл .env. Шаблон .env.example содержит следующие переменные:

### .env
#### Database
    POSTGRES_DB=myproject
    POSTGRES_USER=user
    POSTGRES_PASSWORD=changeme
    DB_HOST=db
    DB_PORT=5432

#### Django
    SECRET_KEY=your-secret-key-here
    DEBUG=False
    ALLOWED_HOSTS=localhost,127.0.0.1

#### Redis
    REDIS_URL=redis://redis:6379/0

#### Celery
    CELERY_BROKER_URL=redis://redis:6379/0
    CELERY_RESULT_BACKEND=redis://redis:6379/0

### Важно: не коммитьте файл .env в репозиторий. Он добавлен в .gitignore.

## Документация:

    Для получения дополнительной информации обратитесь в службу поддержки по телефонам указанным в контактах.

## Лицензия
    
     Проект выполнен по лицензии MIT

## Автор

### Чекунов Александр Николаевич

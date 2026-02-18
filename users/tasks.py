from celery import shared_task
from django.utils import timezone
from django.contrib.auth import get_user_model
from datetime import timedelta

User = get_user_model()


@shared_task
def block_inactive_users():
    # Определяем порог неактивности (30 дней)
    month_ago = timezone.now() - timedelta(days=30)

    # Фильтруем активных пользователей, которые не заходили более месяца
    # last_login__lte — "меньше или равно"
    inactive_users = User.objects.filter(
        last_login__lte=month_ago,
        is_active=True
    )

    count = inactive_users.count()
    inactive_users.update(is_active=False)

    return f"Заблокировано пользователей: {count}"

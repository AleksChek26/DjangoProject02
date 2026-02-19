from datetime import timedelta

from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.utils import timezone

from config import settings
from materials.models import Subscription

User = get_user_model()


@shared_task
def block_inactive_users():
    # Определяем порог неактивности (30 дней)
    month_ago = timezone.now() - timedelta(days=30)

    # Фильтруем активных пользователей, которые не заходили более месяца
    # last_login__lte — "меньше или равно"
    inactive_users = User.objects.filter(last_login__lte=month_ago, is_active=True)

    count = inactive_users.count()
    inactive_users.update(is_active=False)

    return f"Заблокировано пользователей: {count}"


@shared_task
def send_course_update_emails(course_id, course_name):
    subscribers = Subscription.objects.filter(course_id=course_id).values_list(
        "user__email", flat=True
    )

    if subscribers:
        send_mail(
            subject=f"Обновление курса: {course_name}",
            message=f'В курсе "{course_name}" появились новые материалы.',
            from_email=settings.DEFAULT_FROM_EMAIL,  # Используем из настроек
            recipient_list=list(subscribers),
            fail_silently=False,
        )

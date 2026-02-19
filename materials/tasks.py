from celery import shared_task
from django.core.mail import send_mail

from .models import Subscription


@shared_task
def send_course_update_emails(course_id, course_name):
    # Получаем список email-адресов подписчиков
    subscribers = Subscription.objects.filter(course_id=course_id).values_list(
        "user__email", flat=True
    )

    for email in subscribers:
        send_mail(
            subject=f"Обновление курса: {course_name}",
            message=f'В курсе "{course_name}" появились новые материалы. Заходите скорее!',
            from_email="noreply@yourlearning.ru",
            recipient_list=[email],
            fail_silently=False,
        )

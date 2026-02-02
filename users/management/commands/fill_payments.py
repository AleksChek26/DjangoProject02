from django.contrib.auth import get_user_model
from django.core.management import BaseCommand

from users.models import Payment


class Command(BaseCommand):
    def handle(self, *args, **options):
        User = get_user_model()
        user = User.objects.first()  # Берем первого доступного пользователя

        if not user:
            self.stdout.write("Пользователей не найдено")
            return

        Payment.objects.create(user=user, amount=2500, payment_method=Payment.TRANSFER)

        self.stdout.write(self.style.SUCCESS("Данные успешно загружены"))

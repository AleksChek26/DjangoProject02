from django.contrib.auth.models import Group
from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        group, created = Group.objects.get_or_create(name="Moderators")
        if created:
            self.stdout.write(self.style.SUCCESS('Группа "Moderators" создана'))
        else:
            self.stdout.write(self.style.WARNING("Группа уже существует"))

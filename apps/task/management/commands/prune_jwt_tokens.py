from django.core.management import call_command
from django.core.management.base import BaseCommand
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken


class Command(BaseCommand):
    help = "Удаляет истёкшие JWT-токены при достижении 10 000 записей."

    def handle(self, *args, **options):
        if OutstandingToken.objects.count() >= 10_000:
            call_command("flushexpiredtokens")
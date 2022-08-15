from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = (
        "This command using for call 'compilemessages' with flags:\n"
        '--ignore=venv'
    )

    def handle(self, *args, **options):
        call_command("compilemessages", '--ignore=venv')

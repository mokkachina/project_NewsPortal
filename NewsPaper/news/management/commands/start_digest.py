from django.core.management.base import BaseCommand
from news.tasks import start_scheduler


class Command(BaseCommand):
    help = 'Start the weekly digest scheduler'

    def handle(self, *args, **options):
        start_scheduler()
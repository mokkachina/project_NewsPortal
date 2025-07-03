from django.apps import AppConfig
import redis
from django.conf import settings


class NewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news'

    def ready(self):
        if not settings.DEBUG:  # Теперь settings будет доступен
            try:
                from .tasks import start_scheduler
                start_scheduler()
            except Exception as e:
                import logging
                logger = logging.getLogger(__name__)
                logger.error(f"Failed to start scheduler: {e}")
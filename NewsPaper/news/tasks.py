import warnings
from celery import shared_task
import time
import logging
from django_apscheduler.jobstores import DjangoJobStore
from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from apscheduler.schedulers.background import BackgroundScheduler
from django.utils import timezone
from django.urls import reverse
from news.models import Post, Category, Subscription
import datetime
from datetime import timedelta
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.db.models.signals import m2m_changed
from django.template.loader import render_to_string
from zoneinfo import ZoneInfo


logger = logging.getLogger(__name__)

logger = logging.getLogger('news.tasks')

# Подавляем предупреждения pytz
warnings.filterwarnings(
    "ignore",
    category=DeprecationWarning,
    module="apscheduler.util"
)

@shared_task
def send_notifications(preview, pk, title, subscribers):
    html_content = render_to_string(
        'post_create_email.html',
        {
            'text':  preview,
            'link': f'{settings.SITE_URL}/news/{pk}',
        }
    )
    msg = EmailMultiAlternatives(
        subject=title,
        body="",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,

     )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()



@shared_task
def my_work():

    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(dataCreation__gte=last_week)
    # print(posts)
    categories = set(posts.values_list('postCategory__name', flat=True))

    subscribers = set(Category.objects.filter(name__in=categories).values_list('subscribers__email', flat=True))

    html_content = render_to_string(
        'daily_post.html',
        {
            'link': settings.SITE_URL,
            'posts': posts,
        }
    )
    msg = EmailMultiAlternatives(
        subject='Статьи за неделю',
        body="",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,

    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


warnings.filterwarnings(
    action="ignore",
    category=UserWarning,
    module="apscheduler.util"
)

warnings.filterwarnings(
    "ignore",
    category=DeprecationWarning,
    module="apscheduler.util"
)




def send_weekly_digest():
    """Функция для отправки еженедельного дайджеста подписчикам"""
    try:
        logger.info("Запуск еженедельной рассылки...")

        moscow_tz = ZoneInfo('Europe/Moscow')
        now = timezone.now().astimezone(moscow_tz)
        week_ago = now - timedelta(days=7)

        logger.debug(f"Период рассылки: с {week_ago} по {now}")

        for category in Category.objects.all():
            logger.debug(f"Обработка категории: {category.name}")

            new_posts = Post.objects.filter(
                postCategory=category,
                dataCreation__gte=week_ago
            ).order_by('-dataCreation')

            if not new_posts.exists():
                logger.debug(f"Нет новых статей в категории {category.name}")
                continue

            subscriptions = Subscription.objects.filter(
                category=category,
                subscribed=True
            ).select_related('user')

            if not subscriptions.exists():
                logger.debug(f"Нет подписчиков для категории {category.name}")
                continue

            subject = f'📰 Еженедельный дайджест: {category.name}'
            message_lines = [
                f'Новые статьи за неделю ({week_ago.strftime("%d.%m")}-{now.strftime("%d.%m.%Y")}):',
                ''
            ]

            for post in new_posts:
                post_time = post.dataCreation.astimezone(moscow_tz)
                message_lines.extend([
                    f"→ {post.title}",
                    f"  📅 {post_time.strftime('%d.%m %H:%M')}",
                    f"  🔗 http://127.0.0.1:8000{reverse('new_detail', args=[post.id])}",
                    ''
                ])

            message = '\n'.join(message_lines)
            logger.debug(f"Сформировано письмо для категории {category.name}")

            for subscription in subscriptions:
                try:
                    send_mail(
                        subject=subject,
                        message=message,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[subscription.user.email],
                        fail_silently=False,
                    )
                    logger.info(f"Письмо отправлено для {subscription.user.email}")
                except Exception as e:
                    logger.error(
                        f"Ошибка отправки для {subscription.user.email}: {str(e)}",
                        exc_info=True
                    )

        logger.info("Еженедельная рассылка завершена")

    except Exception as e:
        logger.error(
            f"Критическая ошибка в send_weekly_digest: {str(e)}",
            exc_info=True
        )
        raise


def start_scheduler():
    """Запуск планировщика задач"""
    try:
        logger.info("Инициализация планировщика...")

        scheduler = BackgroundScheduler(timezone='Europe/Moscow')
        scheduler.add_jobstore(DjangoJobStore(), 'default')

        scheduler.add_job(
            send_weekly_digest,
            trigger='cron',
            day_of_week='fri',
            hour=18,
            minute=0,
            id='weekly_digest',
            replace_existing=True,
        )

        scheduler.start()
        logger.info("Планировщик успешно запущен")
        return scheduler

    except Exception as e:
        logger.error(
            f"Ошибка запуска планировщика: {str(e)}",
            exc_info=True
        )
        raise


class Command(BaseCommand):
    """Management-команда для запуска рассылки"""
    help = 'Запуск еженедельной рассылки новых статей'

    def handle(self, *args, **options):
        # Используем отдельный логгер для команд
        cmd_logger = logging.getLogger('news.management')
        cmd_logger.info("Запуск команды рассылки")

        try:
            self.stdout.write(self.style.SUCCESS('Запуск планировщика рассылки...'))

            scheduler = start_scheduler()
            cmd_logger.info("Планировщик рассылки запущен")

            self.stdout.write(
                self.style.SUCCESS('✅ Рассылка настроена на каждую пятницу в 18:00 (Мск)')
            )
            self.stdout.write('Для остановки нажмите Ctrl+C')

            # Бесконечный цикл для работы в консоли
            while True:
                pass

        except KeyboardInterrupt:
            if 'scheduler' in locals():
                scheduler.shutdown()
            cmd_logger.info("Рассылка остановлена по запросу пользователя")
            self.stdout.write(self.style.SUCCESS('\nРассылка остановлена'))
        except Exception as e:
            cmd_logger.error(
                f"Ошибка в команде рассылки: {str(e)}",
                exc_info=True
            )
            self.stdout.write(self.style.ERROR(f'Ошибка: {e}'))
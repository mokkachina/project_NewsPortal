import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPaper.settings')

app = Celery('NewsPaper')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
app.conf.beat_schedule = {
    'print_every_10_seconds': {
        'task': 'news.tasks.send_notifications',
        'schedule': crontab(10),
        'args': (),
    },
}

app.conf.beat_schedule = {
    'action_every_monday_8am': {
        'task': 'news.tasks.my_work',
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
        'args': (),
    },
}


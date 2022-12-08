from django.conf import *
from django.dispatch import receiver
from django.db.models.signals import m2m_changed, post_save
from news.models import PostCategory, Post
from django.template.loader import render_to_string
from NewsPaper.settings import *
from django.core.mail import EmailMultiAlternatives
from news.tasks import send_notifications


@receiver(m2m_changed, sender=PostCategory)
def notify_about_new_post(sender, instance, **kwargs):

    if kwargs['action'] == 'post_add':
        categories = instance.postCategory.all()
        subscribers: list[str] = []
        for category in categories:
            subscribers += category.subscribers.all()



        subscribers = [s.email for s in subscribers]
        send_notifications.apply_async((instance.preview(), instance.pk, instance.title, subscribers), countdown=10,)


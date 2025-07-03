from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.urls import reverse
from django.core.validators import MinValueValidator
from django.core.cache import cache
from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy as lz
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings

class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    rating_user = models.SmallIntegerField(default=0)

    def update_rating(self):
        postRat = self.post_set.aggregate(postRating=Sum('rating'))
        pRat = 0
        pRat += postRat.get("postRating")
        commentRat = self.authorUser.comment_set.aggregate(commentRating=Sum('rating'))
        cRat = 0
        cRat += commentRat.get('commentRating')
        self.rating_user = pRat * 3 + cRat
        self.save()

    def __str__(self):
        return f'{self.authorUser}'




class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)
    subscribers = models.ManyToManyField(User, related_name='old_categories')  # старое поле
    new_subscribers = models.ManyToManyField(
        User,
        through='Subscription',
        related_name='categories'
    )


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    NEWS = 'NW'
    ARTICLE = 'AR'
    CATEGORY_CHOICES = (
        (NEWS, lz('News')),
        (ARTICLE, lz('Articles')),
    )
    categoryType = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=ARTICLE)
    dataCreation = models.DateTimeField(auto_now_add=True)
    postCategory = models.ManyToManyField(Category, through='PostCategory', verbose_name='Категория')
    title = models.CharField(max_length=128)
    text = models.TextField()
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()
    def dislike(self):
        self.rating -= 1
        self.save()
    def preview(self):
        return self.text[0:123] + "..."

    def __str__(self):
        return f'{self.author.authorUser.username}: {self.title}: {self.categoryType}: {self.postCategory}'

    # def __str__(self):
    #     return f' {self.postCategory.name}'

    # def get_success_url(self):
    #     return reverse('new_create', kwargs={'pk': self.kwargs['pk']})
    def get_absolute_url(self):
        return reverse('new_detail', args=[str(self.id)])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # сначала вызываем метод родителя, чтобы объект сохранился
        cache.delete(f'product-{self.pk}')  # затем удаляем его из кэша, чтобы сбросить его

class PostCategory(models.Model):
    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)


    def __str__(self):
        return f'{self.postThrough}: {self.categoryThrough}'


class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    dataCreation = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return f'{self.commentPost}: {self.commentUser}: {self.text}: {self.dataCreation}: {self.rating}'

class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    subscribed = models.BooleanField(default=True)
    date_subscribed = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'category')

@receiver(m2m_changed, sender=Post.postCategory.through)
def notify_subscribers(sender, instance, action, **kwargs):
    if action == "post_add":
        # Получаем все категории поста
        for category in instance.postCategory.all():
            # Получаем всех подписчиков через промежуточную модель
            subscriptions = Subscription.objects.filter(category=category, subscribed=True)
            for subscription in subscriptions:
                send_mail(
                    subject=f'Новая публикация в категории {category.name}',
                    message=f'Добавлена новая публикация: "{instance.title}"\n\n'
                           f'Читать: http://127.0.0.1:8000{instance.get_absolute_url()}',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[subscription.user.email],
                    fail_silently=True,
                )
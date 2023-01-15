# Generated by Django 4.1 on 2023-01-13 05:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("news", "0002_category_subscribers_alter_post_postcategory"),
    ]

    operations = [
        migrations.AddField(
            model_name="author",
            name="authorUser_en_us",
            field=models.OneToOneField(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="author",
            name="authorUser_ru",
            field=models.OneToOneField(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="author",
            name="rating_user_en_us",
            field=models.SmallIntegerField(default=0, null=True),
        ),
        migrations.AddField(
            model_name="author",
            name="rating_user_ru",
            field=models.SmallIntegerField(default=0, null=True),
        ),
        migrations.AddField(
            model_name="comment",
            name="commentPost_en_us",
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.CASCADE, to="news.post"
            ),
        ),
        migrations.AddField(
            model_name="comment",
            name="commentPost_ru",
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.CASCADE, to="news.post"
            ),
        ),
        migrations.AddField(
            model_name="comment",
            name="commentUser_en_us",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="comment",
            name="commentUser_ru",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="comment",
            name="dataCreation_en_us",
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name="comment",
            name="dataCreation_ru",
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name="comment",
            name="rating_en_us",
            field=models.SmallIntegerField(default=0, null=True),
        ),
        migrations.AddField(
            model_name="comment",
            name="rating_ru",
            field=models.SmallIntegerField(default=0, null=True),
        ),
        migrations.AddField(
            model_name="comment", name="text_en_us", field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name="comment", name="text_ru", field=models.TextField(null=True),
        ),
    ]
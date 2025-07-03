from django.contrib import admin

from django.contrib import admin
from .models import Post, Author, Comment, PostCategory, Category
from modeltranslation.admin import TranslationAdmin
from .models import*


class PostAdmin(admin.ModelAdmin):
    # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице с новостями
    list_display = ('categoryType', 'title', 'text', 'dataCreation')
    list_filter = ('author', 'categoryType', 'dataCreation')  # добавляем примитивные фильтры в нашу админку
    # search_fields = ('postCategory', 'Category__name')

class PostAdmin(TranslationAdmin):
    model = Post

class AuthorAdmin(TranslationAdmin):
    model = Author

class CommentAdmin(TranslationAdmin):
    model = Comment

class CategorytAdmin(TranslationAdmin):

    model = Category
@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'subscribed', 'date_subscribed')

admin.site.register(Post, PostAdmin)
admin.site.register(Author)
admin.site.register(Comment)
admin.site.register(PostCategory)
admin.site.register(Category)

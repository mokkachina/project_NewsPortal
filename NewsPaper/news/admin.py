from django.contrib import admin

from django.contrib import admin
from .models import Post, Author, Comment, PostCategory, Category


class PostAdmin(admin.ModelAdmin):
    # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице с новостями
    list_display = ('categoryType', 'title', 'text', 'dataCreation')
    list_filter = ('author', 'categoryType', 'dataCreation')  # добавляем примитивные фильтры в нашу админку
    # search_fields = ('postCategory', 'Category__name')

admin.site.register(Post, PostAdmin)
admin.site.register(Author)
admin.site.register(Comment)
admin.site.register(PostCategory)
admin.site.register(Category)

from django.contrib import admin

from django.contrib import admin
from .models import Post, Author, Comment, PostCategory


admin.site.register(Post)
admin.site.register(Author)
admin.site.register(Comment)
admin.site.register(PostCategory)

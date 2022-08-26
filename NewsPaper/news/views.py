from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import*
from datetime import datetime
from pprint import pprint

class NewsPaper(ListView):
    # queryset = Post.objects.filter(rating__lt=20.0).values('author')
    model = Post
    # ordering = "dataCreation"
    #  queryset = Post.objects.all()


    template_name = 'news.html'
    context_object_name = 'news'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        # context['next_sale'] = None
        # pprint(context)
        return context

class NewsDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    model = Post
    # Используем другой шаблон — product.html
    template_name = 'news_title.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'news_title'
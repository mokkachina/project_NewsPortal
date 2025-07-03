from django.urls import path
# Импортируем созданное нами представление
from .views import*
from django.views.decorators.cache import cache_page
from .forms import create_post
urlpatterns = [
   # path — означает путь.
   # В данном случае путь ко всем товарам у нас останется пустым,
   # чуть позже станет ясно почему.
   # Т.к. наше объявленное представление является классом,
   # а Django ожидает функцию, нам надо представить этот класс в виде view.
   # Для этого вызываем метод as_view.
    path('', cache_page(60*1)(NewsPaper.as_view()), name='new_list'),
    path('<int:pk>', cache_page(60*5)(NewsDetail.as_view()), name='new_detail'),
    path('<int:pk>', PostSearch.as_view()),
    path('search/', PostSearch.as_view(), name='new_search'),
    path('create/', PostCreate.as_view(), name='new_create'),

    path('<int:pk>/edit/', PostEdit.as_view(), name='new_edit'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='new_delete'),

    # path('articles/', ArticlesPaper.as_view, name='article_list'),
    path('categories/<int:pk>/', CategoryListView.as_view(), name='category_list'),
    path('subscriptions/', SubscriptionView.as_view(), name='subscriptions'),
    path('subscribe/<int:pk>/', subscribe, name='subscribe'),
    path('<int:pk>/', NewsDetail.as_view(), name='new_detail')
    # path('categories/<int:pk>/subscribers', subscribe_delete, name='subscribe_delete'),
   # path('', IndexView.as_view()),
]

#     path('articles/create/', PostCreateArticles.as_view(), name='post_ar_create'),
#     path('articles/<int:pk>/edit/', PostEdit.as_view(), name='post_ar_edit'),
#     path('articles/<int:pk>/delete/', PostDelete.as_view(), name='post_ar_delete'),


from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import*
from .filters import PostFilter
from datetime import datetime, timedelta
from django.views.generic import FormView, CreateView, UpdateView, DeleteView, View
from .forms import PostForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.http import HttpResponse, HttpResponseNotFound
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
import logging
from django.utils.translation import gettext as _
from django.utils.translation import pgettext_lazy
from django.utils import timezone
from django.shortcuts import redirect


import pytz #  импортируем стандартный модуль для работы с часовыми поясами


logger = logging.getLogger(__name__)


# from .tasks import hello, printer
from django.core.mail import send_mail
from pprint import pprint

# class IndexView(View):
#     def get(self, request):
#         printer.apply_async([10],
#                             eta = datetime.now() + timedelta(seconds=5))
#         hello.delay()
#         return HttpResponse('Hello!')

class NewsPaper(ListView):
    # queryset = Post.objects.filter(rating__lt=20.0).values('author')

    model = Post
    # ordering = "categoryType"
    # queryset = Post.objects.get('NW')


    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10




    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs


    def get_context_data(self, **kwargs):
        current_time = timezone.localtime(timezone.now())
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        context['current_time'] = current_time
        context['timezones'] = pytz.common_timezones
        # pprint(context)
        return context

    # def set_timezone(self, request):
    #     if request.method == 'POST':
    #         request.session['django_timezone'] = request.POST['timezone']
    #         return redirect('/')
    #     else:
    #         return render(request, 'news.html', {'timezones': pytz.common_timezones})
    def post(self, request):
        request.session['django_timezone'] = request.POST['timezone']
        return redirect('/')

    def pageNotFound(request, exception):
        return HttpResponseNotFound('<h1>Страница не найдена </h1>')



class ArticlesPaper(ListView):
    queryset = Post.objects.filter(categoryType='AR')
    model = Post
    # ordering = "categoryType"
    # queryset = Post.objects.get('NW')


    template_name = 'articles.html'
    context_object_name = 'articl'
    paginate_by = 10

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     self.filterset = PostFilter(self.request.GET, queryset)
    #     return self.filterset.qs
    #
    #
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['filterset'] = self.filterset
    #     # context['time_now'] = datetime.utcnow()
    #     # context['next_sale'] = None
    #     # pprint(context)
    #     return context

class NewsDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному
    model = Post

    template_name = 'news_detail.html'
    # Название объекта, в котором будет выбранный пользователем
    context_object_name = 'new_detail'

class PostSearch(ListView):

    model = Post
    # ordering = ['-date']
    template_name = 'search.html'
    context_object_name = 'search'
    paginate_by = 10
    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs
    def get_context_data(self, **kwargs):
        current_time = timezone.localtime(timezone.now())
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        context['current_time'] = timezone.now()
        context['timezones'] = pytz.common_timezones
        # datetime.utcnow()
        return context

    def post(self, request):
        request.session['django_timezone'] = request.POST['timezone']
        return redirect('/search')


class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    # Указываем нашу разработанную форму
    form_class = PostForm
    # модель товаров
    model = Post
    # и новый шаблон, в котором используется форма.
    template_name = 'create.html'

    # def form_valid(self, form):
    #     categoryType = form.save(commit=False)
    #     categoryType.name = 'Новость'
    #     return super().form_valid(form)


class PostEdit(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'create.html'

class PostDelete(PermissionRequiredMixin,DeleteView):
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'delete.html'
    context_object_name = 'news'
    success_url = reverse_lazy('new_list')

class ProtectedView(LoginRequiredMixin, TemplateView):
    raise_exception = True
    template_name = 'prodected_page.html'

class CategoryListView(ListView):

    model = Post
    template_name = 'category_list.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.postCategory = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(postCategory=self.postCategory).order_by('-dataCreation')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.postCategory.subscribers.all()
        context['category'] = self.postCategory
        return context


@login_required
def subscribe(request, pk):
    category = get_object_or_404(Category, id=pk)

    if request.method == 'POST':
        action = request.POST.get('action', 'subscribe')

        if action == 'subscribe':
            Subscription.objects.get_or_create(
                user=request.user,
                category=category,
                defaults={'subscribed': True}
            )
        elif action == 'unsubscribe':
            Subscription.objects.filter(
                user=request.user,
                category=category
            ).update(subscribed=False)

    return redirect('subscriptions')

class SubscriptionView(LoginRequiredMixin, ListView):
    model = Subscription
    template_name = 'subscribtions.html'  # Указываем явный путь к шаблону
    context_object_name = 'subscriptions'

    def get_queryset(self):
        return Subscription.objects.filter(user=self.request.user, subscribed=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_categories'] = Category.objects.all()
        return context

# @login_required
# def subscribe_delete(request, pk):
#     user = request.user
#     category = Category.objects.get(id=pk)
#     category.subscribers.remove(user)
#
#     message = 'Вы отписались от: '
#     return render(request, 'subscribe_delete.html', {'message': message, 'category': category})
# @login_required
# def upgrade_user(request):
#     user = request.user
#     group = Group.objects.get(name='authors')
#     if not request.user.groups.filter(name='authors').exists():
#         group.user_set.add(user)
#         if not hasattr(user, 'author'):
#             Author.objects.create(
#                 authorUser=User.objects.get(pk=user.id)
#             )
#     return redirect('/')




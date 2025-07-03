from django_filters import FilterSet, ModelChoiceFilter, DateFilter
from .models import Post, Category
from django.forms.widgets import DateInput
from django.utils.translation import gettext_lazy as _


class PostFilter(FilterSet):
    postCategory = ModelChoiceFilter(
        lookup_expr='exact',
        queryset=Category.objects.all(),
        label=_('Category'),
        empty_label=_('all'),
    )

    date = DateFilter(
        field_name='dataCreation',
        lookup_expr='gt',
        label=_('Create after'),
        widget=DateInput(attrs={'type': 'date'}))

    date.field.error_messages = {'invalid': 'Enter date in format DD.MM.YYYY.Example: 31.12.2020'}
    date.field.widget.attrs = {'placeholder': 'DD.MM.YYYY'}

    class Meta:

        model = Post
        fields = {

            #     # поиск по названию
            'title': ['icontains'],
            #     # 'text': ['icontains'],
            #     # 'postCategory': ['icontains'],
            #     'dataCreation': ['year__lt'],
        }

        labels = {
            'title': _('title'),
            }


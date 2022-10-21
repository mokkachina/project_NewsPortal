from django_filters import FilterSet, ModelChoiceFilter, DateFilter
from .models import Post, Category
from django.forms.widgets import DateInput


class PostFilter(FilterSet):
    postCategory = ModelChoiceFilter(
        lookup_expr='exact',
        queryset=Category.objects.all(),
        label='Category',
        empty_label='all',
    )

    date = DateFilter(
        field_name='dataCreation',
        lookup_expr='gt',
        label='Create after',
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




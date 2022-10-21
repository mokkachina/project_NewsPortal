from django import forms
from .models import Post
from django.shortcuts import render
from django.http import*
from django.core.exceptions import ValidationError


class PostForm(forms.ModelForm):
   class Meta:
       model = Post
       fields = [
          'author',
          'categoryType',
          'postCategory',
          'title',
          'text',
       ]

def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/news')

    form = PostForm()

    return render(request, 'create.html', {'form': form})

def create_edit(request):

    pass


def create_delete(request):
    pass
# class ProductForm(forms.Form):
#     name = forms.CharField(label='Name')
#     description = forms.CharField(label='Description')
#     quantity = forms.IntegerField(label='Quantity')
#     category = forms.ModelChoiceField(
#         label='Category', queryset=Category.objects.all(),
#     )
#     price = forms.FloatField(label='Price')
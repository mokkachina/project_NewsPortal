from django import forms
from .models import Post
from django.shortcuts import render
from django.http import*
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
# from django.utils.translation import gettext as _


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
       labels = {
           'author': _('author'),
           'categoryType': _('categoryType'),
           'postCategory': _('postCategory'),
           'title': _('title'),
           'text': _('text'),
       }

def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/news')

    form = PostForm()

    return render(request, 'create.html', {'form': form})

# def create_edit(request):
#
#     pass

#
# def create_delete(request):
#     pass
# class PostForm(forms.Form):
#     author = forms.CharField(label='Name')
#     categoryType = forms.CharField(label='Description')
#     title = forms.IntegerField(label='Quantity')
#     postCategory = forms.ModelChoiceField(
#         label='Category', queryset=Category.objects.all(),
#     )
#     text = forms.FloatField(label='Price')
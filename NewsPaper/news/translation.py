from .models import *
from modeltranslation.translator import register, TranslationOptions

#
@register(Post)
class PostTranslationOptions(TranslationOptions):
    fields = (
        'categoryType',
        'dataCreation',
        'title',
        'text',
             )  # указываем, какие именно поля надо переводить в виде кортежа


@register(Author)
class AuthorTranslationOptions(TranslationOptions):
    fields = ('authorUser', 'rating_user')


@register(Comment)
class CommentTranslationOptions(TranslationOptions):
    fields = ('commentPost', 'commentUser', 'text', 'dataCreation', 'rating')


# @register(PostCategory)
# class PostCategoryTranslationOptions(TranslationOptions):
#     fields = ('postThrough', 'categoryThrough')


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)


from django.core.management.base import BaseCommand, CommandError

from news.models import Category, Post


class Command(BaseCommand):
    help = 'Подсказка вашей команды python manage.py delcategory Sport'


    def add_arguments(self, parser):
        parser.add_argument('Category', type=str)

    def handle(self, *args, **options):
        answer = input(
            f'Вы правда хотите удалить все статьи в категории {options["Category"]}? yes/no')

        if answer != 'yes':
            self.stdout.write(self.style.ERROR('Отменено'))
        else:
            try:
                category = Category.objects.get(name=options['Category'])
                Post.objects.filter(postCategory=category).delete()
                # в случае неправильного подтверждения говорим, что в доступе отказано
                self.stdout.write(self.style.SUCCESS(
                    f'Все новости в категории {category.name} успешно удалены'))
            except category.DoesNotExist:
                self.stdout.write(self.style.ERROR(
                    f'Не удалось найти категорию {category.name}'))


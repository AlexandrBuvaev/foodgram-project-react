from django.core.management import BaseCommand

from recipes.models import Tag


class Command(BaseCommand):
    help = 'Загрузка подготовленных тегов.'

    def handle(self, *args, **kwargs):
        data = [
            {'name': 'Завтрак', 'color': '#EC6E19', 'slug': 'breakfast'},
            {'name': 'Обед', 'color': '#DB04E9', 'slug': 'dinner'},
            {'name': 'Ужин', 'color': '#364236', 'slug': 'evening_meal'}
        ]
        Tag.objects.bulk_create(
            Tag(**value) for value in data)
        self.stdout.write(self.style.SUCCESS('Все теги загружены.'))

from django.core.management import BaseCommand
from mainapp.models import News


class Command(BaseCommand):
    def handle(self, *args, **options):
        news_list=[]
        for i in range(10):
            news_list.append(News(
                title=f"title_{i}",
                preambule=f"intro_{i}",
                body=f'body_{i}'
            ))
        News.objects.bulk_create(news_list)

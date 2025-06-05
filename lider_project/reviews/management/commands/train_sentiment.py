from django.core.management.base import BaseCommand
from reviews.train_sentiment_model import main

class Command(BaseCommand):
    help = 'Обучает модель анализа тональности на существующих отзывах'

    def handle(self, *args, **options):
        self.stdout.write('Начинаем обучение модели...')
        main()
        self.stdout.write(self.style.SUCCESS('Обучение модели завершено!')) 
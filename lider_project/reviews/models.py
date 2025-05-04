import sys

from django.db import models
from deeppavlov import build_model

sentiment_model = build_model("rusentiment_bert", download=True)

def get_sentiment_model():
    if 'makemigrations' not in sys.argv and 'migrate' not in sys.argv:
        return build_model("rusentiment_bert", download=True)
    return None

class Review(models.Model):
    text = models.TextField(verbose_name="Текст отзыва")
    sentiment = models.CharField(max_length=20, blank=True, null=True, verbose_name="Тональность", )

    def save(self, *args, **kwargs):
        result = sentiment_model([self.text])[0]
        self.sentiment = result

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Отзыв: {self.text[:30]}..."

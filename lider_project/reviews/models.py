import sys
import os
import logging
from functools import lru_cache
from django.db import models
from django.core.cache import cache
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

logger = logging.getLogger(__name__)
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'trained_model')

# Словарь для маппинга меток
LABEL_MAPPING = {
    0: "negative",    # Отрицательный
    1: "neutral",     # Нейтральный
    2: "positive"     # Положительный
}

@lru_cache(maxsize=1)
def load_sentiment_model():
    try:
        if 'makemigrations' not in sys.argv and 'migrate' not in sys.argv:
            tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
            model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
            model.eval()
            return model, tokenizer
    except Exception as e:
        logger.error(f"Ошибка загрузки модели: {str(e)}")
    return None, None

def get_sentiment(text):
    cache_key = f"sentiment_{hash(text)}"
    cached_result = cache.get(cache_key)
    if cached_result is not None:
        return cached_result

    model, tokenizer = load_sentiment_model()
    if model is None or tokenizer is None:
        return "unknown"

    try:
        # Добавляем отладочную информацию
        logger.info(f"Анализ текста: {text}")
        
        inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
        with torch.no_grad():
            outputs = model(**inputs)
            predictions = torch.softmax(outputs.logits, dim=1)
            
            # Получаем вероятности для каждого класса
            probs = predictions[0].tolist()
            logger.info(f"Вероятности классов: {probs}")
            
            # Определяем тональность на основе вероятностей
            sentiment = torch.argmax(predictions, dim=1).item()
            result = LABEL_MAPPING.get(sentiment, "unknown")
            
            # Если вероятность положительного класса высокая, считаем отзыв положительным
            if probs[2] > 0.4:  # Порог для положительного класса
                result = "positive"
            elif probs[0] > 0.4:  # Порог для отрицательного класса
                result = "negative"
            else:
                result = "neutral"
            
            logger.info(f"Результат классификации: {result} (вероятности: neg={probs[0]:.4f}, neu={probs[1]:.4f}, pos={probs[2]:.4f})")
            cache.set(cache_key, result, timeout=3600)
            return result
            
    except Exception as e:
        logger.error(f"Ошибка при анализе тональности: {str(e)}")
        return "unknown"

class Review(models.Model):
    text = models.TextField(verbose_name="Текст отзыва")
    sentiment = models.CharField(max_length=20, blank=True, null=True, verbose_name="Тональность")

    def save(self, *args, **kwargs):
        if not self.sentiment:
            self.sentiment = get_sentiment(self.text)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Отзыв: {self.text[:30]}..."

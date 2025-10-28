from django.db import models
import requests

class Category(models.Model):
    category_name = models.CharField(max_length=255, verbose_name="Название категории")
    description = models.TextField(max_length=1000, verbose_name="Описание")
    image_url = models.URLField(verbose_name="Изображение")

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")
    product_name = models.CharField(max_length=255, verbose_name="Название продукции")
    description = models.TextField(max_length=1000, verbose_name="Описание продукции")
    cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")

    def __str__(self):
        return self.product_name

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"


class Attribute(models.Model):
    attribute_name = models.CharField(max_length=255, verbose_name="Характеристика")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")

    def __str__(self):
        return self.attribute_name

    class Meta:
        verbose_name = "Характеристика"
        verbose_name_plural = "Характеристики"


class AttributeValue(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Продукт")
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE, verbose_name="Атрибут")
    value = models.CharField(max_length=255, verbose_name="Значение атрибута")

    def __str__(self):
        return f"{self.attribute}: {self.value}"

    class Meta:
        verbose_name = "Значение атрибута"
        verbose_name_plural = "Значения атрибутов"


class ProductImages(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Продукт", related_name='images')
    public_yandex_link = models.URLField(
        verbose_name="Публичная ссылка (Яндекс.Диск)",
        blank=True,
        help_text="Вставьте публичную ссылку Яндекс.Диска, например https://disk.yandex.ru/i/..."
    )
    image_url = models.URLField(
        verbose_name="Прямая ссылка на изображение (заполняется автоматически)",
        blank=True,
        editable=False
    )
    alternative_text = models.CharField(max_length=255, verbose_name="Альтернативный текст")

    def save(self, *args, **kwargs):
        if self.public_yandex_link:
            direct_url = self.get_direct_link_from_public()
            if direct_url:
                self.image_url = direct_url
        super().save(*args, **kwargs)

    def get_direct_link_from_public(self):
        api_url = "https://cloud-api.yandex.net/v1/disk/public/resources/download"
        params = {"public_key": self.public_yandex_link}
        try:
            response = requests.get(api_url, params=params, timeout=5)
            if response.status_code == 200:
                return response.json().get("href")
        except Exception:
            pass
        return None

    def __str__(self):
        return self.alternative_text or "Изображение"

    class Meta:
        verbose_name = "Изображение продукции"
        verbose_name_plural = "Изображения продукции"
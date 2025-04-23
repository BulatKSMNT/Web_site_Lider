from django.db import models

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
        verbose_name = "Атрибут"
        verbose_name_plural = "Атрибуты"


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
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Продукт")
    image_url = models.URLField(verbose_name="Изображение")
    alternative_text = models.CharField(max_length=255, verbose_name="Альтернативный текст")

    def __str__(self):
        return self.alternative_text

    class Meta:
        verbose_name = "Изображение продукта"
        verbose_name_plural = "Изображения продуктов"
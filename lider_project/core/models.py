from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField

class Request(models.Model):
    fullname = models.CharField(max_length=255, verbose_name="ФИО")
    phone_number = PhoneNumberField(verbose_name="Номер телефона")
    email = models.EmailField(max_length=255, verbose_name="Email")
    description = models.TextField(max_length=1000, verbose_name="Сообщение", blank=True, null=True)
    created_at = models.DateTimeField(
        verbose_name='Дата и время создания',
        auto_now_add=True,
        editable=False
    )
    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('processed', 'В обработке'),
        ('completed', 'Завершена'),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new',
        verbose_name="Статус заявки"
    )


    def __str__(self):
        return f"{self.fullname} - {self.phone_number}"

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"
        ordering = ['-created_at']  # Сортировка по дате создания (новые сначала)
        indexes = [
            models.Index(fields=['status']),  # Индекс для статуса
            models.Index(fields=['created_at']),  # Индекс для даты
        ]

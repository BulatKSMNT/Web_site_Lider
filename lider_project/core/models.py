from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

class Request(models.Model):
    fullname = models.CharField(max_length=255, verbose_name="ФИО")
    phone_number = PhoneNumberField(verbose_name="Номер телефона")
    email = models.EmailField(max_length=255, verbose_name="Email")
    description = models.TextField(max_length=1000, verbose_name="Сообщение", blank=True, null=True)

    def __str__(self):
        return f"{self.fullname} - {self.phone_number}"

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"

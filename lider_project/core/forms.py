from django import forms
from django.core.exceptions import ValidationError
from phonenumber_field.formfields import PhoneNumberField
import re


class RequestForm(forms.Form):
    fullname = forms.CharField(label="ФИО")
    phone_number = PhoneNumberField(label="Номер телефона")
    email = forms.EmailField(label="Электронная почта")
    description = forms.CharField(label="Описание",widget=forms.Textarea, required=False)
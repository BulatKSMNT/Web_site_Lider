from django.contrib import admin

from .models import Request

# Register your models here.

@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ('fullname','phone_number','email')
    list_filter = ('fullname','phone_number')

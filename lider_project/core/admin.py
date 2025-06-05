from django.contrib import admin

from .models import Request

# Register your models here.

@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ('created_at','status','fullname','phone_number','email')
    list_filter = ('status','created_at')
    search_fields = ('created_at','fullname')

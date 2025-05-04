from django.contrib import admin
from reviews.models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("text", "sentiment")
    list_filter = ("sentiment",)
    search_fields = ("text",)
    readonly_fields = ("sentiment",)
from django.contrib import admin
from .models import Category, Product, Attribute, AttributeValue, ProductImages

# Register your models here.

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Attribute)
admin.site.register(AttributeValue)
admin.site.register(ProductImages)


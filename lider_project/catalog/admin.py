from django.contrib import admin
from django.utils.html import format_html

from .models import Category, Product, Attribute, AttributeValue, ProductImages


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'image_preview', 'product_count')
    search_fields = ('category_name', 'description')
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image_url:
            return format_html('<img src="{}" width="100" />', obj.image_url)
        return "Нет изображения"

    image_preview.short_description = 'Превью'

    def product_count(self, obj):
        return obj.product_set.count()

    product_count.short_description = 'Кол-во товаров'


class AttributeValueInline(admin.TabularInline):
    model = AttributeValue
    extra = 1
    fields = ('attribute', 'value')
    raw_id_fields = ('attribute',)


class ProductImagesInline(admin.TabularInline):
    model = ProductImages
    extra = 1
    fields = ('image_url', 'image_preview', 'alternative_text')
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image_url:
            return format_html('<img src="{}" width="100" />', obj.image_url)
        return "Нет изображения"

    image_preview.short_description = 'Превью'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'category', 'formatted_cost', 'attribute_values', 'main_image_preview')
    list_filter = ('category',)
    search_fields = ('product_name', 'description')
    inlines = [AttributeValueInline, ProductImagesInline]
    list_per_page = 20

    def formatted_cost(self, obj):
        return f"{obj.cost} ₽"
    formatted_cost.short_description = 'Цена'

    def attribute_values(self, obj):
        return ", ".join([f"{av.attribute}: {av.value}" for av in obj.attributevalue_set.all()[:3]])
    attribute_values.short_description = 'Атрибуты'

    def main_image_preview(self, obj):
        first_image = obj.images.first()
        if first_image and first_image.image_url:
            return format_html('<img src="{}" width="50" />', first_image.image_url)
        return "Нет изображения"
    main_image_preview.short_description = 'Изображение'


@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ('attribute_name', 'category', 'products_count')
    list_filter = ('category',)
    search_fields = ('attribute_name',)

    def products_count(self, obj):
        return obj.attributevalue_set.count()
    products_count.short_description = 'Используется в товарах'


@admin.register(AttributeValue)
class AttributeValueAdmin(admin.ModelAdmin):
    list_display = ('product', 'attribute', 'value')
    list_filter = ('attribute__category', 'attribute')
    search_fields = ('product__product_name', 'value')
    raw_id_fields = ('product', 'attribute')
    list_select_related = ('product', 'attribute')


@admin.register(ProductImages)
class ProductImagesAdmin(admin.ModelAdmin):
    list_display = ('product', 'image_preview', 'alternative_text')
    search_fields = ('product__product_name', 'alternative_text')
    list_filter = ('product__category',)
    raw_id_fields = ('product',)

    def image_preview(self, obj):
        if obj.image_url:
            return format_html('<img src="{}" width="100" />', obj.image_url)
        return "Нет изображения"

    image_preview.short_description = 'Превью'
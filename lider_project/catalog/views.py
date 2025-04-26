from django.db.models import Prefetch
from django.shortcuts import render, get_object_or_404

from catalog.models import Category, Product, ProductImages, Attribute, AttributeValue

def category_list(request):
    categories = Category.objects.all().order_by('category_name')
    return render(request, 'catalog/category_list.html', {"categories" : categories})


def product_list(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category).prefetch_related('images')

    return render(request, 'catalog/product_list.html', {
        'category': category,
        'products': products
    })

def product_detail(request, category_id, product_id):
    category = get_object_or_404(Category, id=category_id)
    product = get_object_or_404(Product, id=product_id, category=category)

    # Получаем изображения продукта (через related_name 'images')
    images = product.images.all()

    attributes = Attribute.objects.filter(category=category)
    attribute_values = AttributeValue.objects.filter(product=product)

    return render(request, 'catalog/product_detail.html', {
        'category' :  category,
        'product': product,
        'images': images,
        'attributes': attributes,
        'attribute_values': attribute_values,
    })
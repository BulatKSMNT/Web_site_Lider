from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils.http import urlencode

from catalog.models import Category, Product, ProductImages, Attribute, AttributeValue

from catalog.forms import SearchForm, CategoryFilterForm

from core.forms import RequestForm

from core.models import Request


def category_list(request):
    categories = Category.objects.all()
    category_search_form = SearchForm(request.GET)

    if category_search_form.is_valid():
        search_query = category_search_form.cleaned_data['search']
        if search_query:
            categories = categories.filter(category_name__icontains=search_query)

    return render(request, 'catalog/category_list.html', {
        "form": category_search_form,
        "categories" : categories
    })


def product_list(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category).prefetch_related('images')

    check_category = CategoryFilterForm(request.GET)
    product_search_form = SearchForm(request.GET)

    if check_category.is_valid() and product_search_form.is_valid():
        selected_category = check_category.cleaned_data['category']
        search_query = product_search_form.cleaned_data['search']

        if selected_category and selected_category.id != category_id:
            query_params = {}
            if search_query:
                query_params['search'] = search_query

            base_url = reverse('product_list', kwargs={'category_id': selected_category.id})
            url = f"{base_url}?{urlencode(query_params)}" if query_params else base_url
            return redirect(url)

        if search_query:
            products = products.filter(product_name__icontains=search_query)

    return render(request, 'catalog/product_list.html', {
        'category': category,
        'products': products,
        'form': product_search_form,
        'check_form': check_category
    })

def product_detail(request, category_id, product_id):
    category = get_object_or_404(Category, id=category_id)
    product = get_object_or_404(Product, id=product_id, category=category)

    # Получаем изображения продукта (через related_name 'images')
    images = product.images.all()

    attributes = Attribute.objects.filter(category=category)
    attribute_values = AttributeValue.objects.filter(product=product)

    alternative_products = (
        Product.objects
        .filter(category=category_id)
        .exclude(id=product_id)  # Исключаем текущий товар
        .order_by('?')[:4]              # Случайная сортировка и лимит 4
    )

    form = RequestForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        Request.objects.create(
            fullname=form.cleaned_data['fullname'],
            phone_number=form.cleaned_data['phone_number'],
            email=form.cleaned_data['email'],
            description=form.cleaned_data['description']
        )
        messages.success(request, "Заявка успешно отправлена! Мы свяжемся с вами.")
        return redirect(request.path)

    return render(request, 'catalog/product_detail.html', {
        'form' : form,
        'category' :  category,
        'product': product,
        'alt_products' : alternative_products,
        'images': images,
        'attributes': attributes,
        'attribute_values': attribute_values,
    })

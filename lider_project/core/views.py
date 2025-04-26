import random

from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect

from core.forms import RequestForm
from core.models import Request
from catalog.models import Category


def user_request(request):
    categories = Category.objects.all().order_by('?')[:6]

    is_success = False
    if request.method == 'POST':
        form = RequestForm(data = request.POST)
        if form.is_valid():
            Request.objects.create(
                fullname=form.cleaned_data['fullname'],
                phone_number=form.cleaned_data['phone_number'],
                email=form.cleaned_data['email'],
                description=form.cleaned_data['description']
            )
            messages.success(request, "Заявка успешно отправлена! Мы свяжемся с вами.")
            return redirect("/#contact")
    else:
        form = RequestForm()

    return render(request, 'core/index.html', {'form': form ,"categories" : categories})
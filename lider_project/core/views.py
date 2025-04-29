from django.contrib import messages
from django.shortcuts import render, redirect
from core.forms import RequestForm
from core.models import Request
from catalog.models import Category

def user_request(request):
    categories = Category.objects.all().order_by('?')[:6]
    form = RequestForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        Request.objects.create(
            fullname=form.cleaned_data['fullname'],
            phone_number=form.cleaned_data['phone_number'],
            email=form.cleaned_data['email'],
            description=form.cleaned_data['description']
        )
        messages.success(request, "Заявка успешно отправлена! Мы свяжемся с вами.")
        return redirect('/')

    return render(request, 'core/index.html', {'form': form, 'categories': categories})

def contact_view(request):
    form = RequestForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        Request.objects.create(
            fullname=form.cleaned_data['fullname'],
            phone_number=form.cleaned_data['phone_number'],
            email=form.cleaned_data['email'],
            description=form.cleaned_data['description']
        )
        messages.success(request, "Заявка успешно отправлена! Мы свяжемся с вами.")
        return redirect('/request/?submitted=1')

    return render(request, 'core/request.html', {'form': form})

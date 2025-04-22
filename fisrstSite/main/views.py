from django.shortcuts import render, get_object_or_404
from .models import AboutPage

def index(request):
    return render(request, 'main/index.html')

def about(request):
    about_page = get_object_or_404(AboutPage, pk=1)  # Берем запись с id=1
    return render(request, 'main/about.html', {'about_page': about_page})
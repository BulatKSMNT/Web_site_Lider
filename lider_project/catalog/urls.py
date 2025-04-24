from tkinter.font import names

from django.urls import path
from . import views

urlpatterns = [
    path('', views.catalog_list, name='catalog_list'),
    path('category/', views.category, name = 'category'),
    path('category/product/', views.product, name = 'product')
]
from django.urls import path
from reviews import views

urlpatterns = [
    path('add/', views.add_review, name='add_review'),
    path('list/', views.reviews_list, name='reviews_list'),
]
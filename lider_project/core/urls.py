from django.urls import path

from . import views
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', views.user_request, name='index'),
    path('admin/', admin.site.urls),
    path('reviews/', include('reviews.urls'))
]

from django.urls import path
from . import views

urlpatterns = [
    path('get/all', views.get_all_country, name='get_all_country'),
    path('get/<int:id>', views.get_country, name='get_country'),
]

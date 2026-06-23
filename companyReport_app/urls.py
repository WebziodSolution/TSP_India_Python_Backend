from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_filtered_companies, name='get_filtered_companies'),
]

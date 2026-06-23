from django.urls import path
from . import views

urlpatterns = [
    path('getAllActions', views.get_all_actions, name='get_all_actions'),
]

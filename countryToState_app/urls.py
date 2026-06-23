from django.urls import path
from . import views

urlpatterns = [
    path('get/all', views.get_all_state, name='get_all_state'),
    path('getAllStateByCountry/<int:id>', views.get_all_state_by_country, name='get_all_state_by_country'),
]

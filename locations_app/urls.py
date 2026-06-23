from django.urls import path
from . import views

urlpatterns = [
    path('getActiveLocations/<str:id>', views.get_company_active_locations, name='get_company_active_locations'),
    path('getAllLocationByCompany/<str:id>', views.get_all_location_by_company, name='get_all_location_by_company'),
    path('get/all', views.get_all_location, name='get_all_location'),
    path('getLocations', views.get_locations, name='get_locations'),
    path('get/<str:id>', views.get_location, name='get_location'),
    path('create', views.create_location, name='create_location'),
    path('update/<str:id>', views.update_location, name='update_location'),
    path('delete/<str:id>', views.delete_location, name='delete_location'),
]

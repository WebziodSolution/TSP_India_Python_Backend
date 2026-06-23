from django.urls import path
from . import views

urlpatterns = [
    path('get/all', views.get_all_employment_info, name='get_all_employment_info'),
    path('get/<int:id>', views.get_employment_info_by_id, name='get_employment_info_by_id'),
    path('create', views.create_employment_info, name='create_employment_info'),
    path('update/<int:id>', views.update_employment_info, name='update_employment_info'),
    path('delete/<int:id>', views.delete_employment_info, name='delete_employment_info'),
]

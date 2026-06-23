from django.urls import path
from . import views

urlpatterns = [
    path('get/All', views.get_all_employee_types, name='get_all_employee_types'),
    path('get/<int:id>', views.get_employee_type, name='get_employee_type'),
    path('create', views.create_employee_type, name='create_employee_type'),
    path('update/<int:id>', views.update_employee_type, name='update_employee_type'),
    path('delete/<int:id>', views.delete_employee_type, name='delete_employee_type'),
]

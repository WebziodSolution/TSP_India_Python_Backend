from django.urls import path
from . import views

urlpatterns = [
    path('get/all/<int:companyId>', views.get_all_leave_types, name='get_all_leave_types'),
    path('get/<int:id>', views.get_leave_type, name='get_leave_type'),
    path('create', views.create_leave_type, name='create_leave_type'),
    path('update/<int:id>', views.update_leave_type, name='update_leave_type'),
    path('delete/<int:id>', views.delete_leave_type, name='delete_leave_type'),
]

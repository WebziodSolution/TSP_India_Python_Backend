from django.urls import path
from . import views

urlpatterns = [
    path('get/all/<int:companyId>', views.get_all_department, name='get_all_department'),
    path('get/<int:id>', views.get_department, name='get_department'),
    path('create', views.create_department, name='create_department'),
    path('update/<int:id>', views.update_department, name='update_department'),
    path('delete/<int:id>', views.delete_department, name='delete_department'),
]

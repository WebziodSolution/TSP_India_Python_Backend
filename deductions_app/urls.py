from django.urls import path
from . import views

urlpatterns = [
    path('get/all', views.get_all_deductions, name='get_all_deductions'),
    path('get/<int:id>', views.get_deductions, name='get_deductions'),
    path('save', views.save_deductions, name='save_deductions'),
    path('delete/<int:id>', views.delete_deductions, name='delete_deductions'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('get/all/<int:companyId>', views.get_all_shifts, name='get_all_shifts'),
    path('get/<int:id>', views.get_shift_by_id, name='get_shift_by_id'),
    path('create', views.create_shift, name='create_shift'),
    path('update/<int:id>', views.update_shift, name='update_shift'),
    path('delete/<int:id>', views.delete_shift, name='delete_shift'),
]

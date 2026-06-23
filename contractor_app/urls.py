from django.urls import path
from . import views

urlpatterns = [
    path('get/all', views.get_all_contractors, name='get_all_contractors'),
    path('get/<int:id>', views.get_contractor, name='get_contractor'),
    path('create', views.create_contractor, name='create_contractor'),
    path('update/<int:id>', views.update_contractor, name='update_contractor'),
    path('delete/<int:id>', views.delete_contractor, name='delete_contractor'),
]

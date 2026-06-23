from django.urls import path
from . import views

urlpatterns = [
    path('getAllFunctionality', views.get_all_functionality, name='get_all_functionality'),
    path('get/<str:id>', views.get_functionality, name='get_functionality'),
    path('create', views.create_functionality, name='create_functionality'),
    path('update/<str:id>', views.update_functionality, name='update_functionality'),
    path('delete/<str:id>', views.delete_functionality, name='delete_functionality'),
]

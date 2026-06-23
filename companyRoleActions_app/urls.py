from django.urls import path
from . import views

urlpatterns = [
    path('get/all', views.get_all_company_role_actions, name='get_all_company_role_actions'),
    path('get/<str:id>', views.get_action, name='get_action'),
    path('create', views.create_action, name='create_action'),
    path('update/<str:id>', views.update_action, name='update_action'),
    path('delete/<str:id>', views.delete_action, name='delete_action'),
]

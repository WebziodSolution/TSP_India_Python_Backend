from django.urls import path
from . import views

urlpatterns = [
    path('get/all/<str:id>', views.get_all_by_company, name='get_all_by_company'),
    path('get/<str:id>', views.get_by_id, name='get_by_id'),
    path('assignEmployees', views.assign_employees, name='assign_employees'),
    path('create', views.create, name='create_weekly_off'),
    path('update/<str:id>', views.update, name='update_weekly_off'),
    path('delete/<str:id>', views.delete, name='delete_weekly_off'),
    path('assignDefaultTemplate/<str:id>', views.assign_default_template, name='assign_default_template'),
]

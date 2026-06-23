from django.urls import path
from . import views

urlpatterns = [
    path('get/all/<int:id>', views.get_all_holiday_templates_by_company_id, name='get_all_holiday_templates_by_company_id'),
    path('get/<int:id>', views.get_holiday_template, name='get_holiday_template'),
    path('create', views.create_holiday_template, name='create_holiday_template'),
    path('update/<int:id>', views.update_holiday_template, name='update_holiday_template'),
    path('delete/<int:id>', views.delete_holiday_template, name='delete_holiday_template'),
    path('assignEmployees', views.assign_employees, name='assign_employees'),
]

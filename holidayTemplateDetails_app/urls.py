from django.urls import path
from . import views

urlpatterns = [
    path('get/all/<int:id>', views.get_all_holiday_template_details_by_template_id, name='get_all_holiday_template_details_by_template_id'),
    path('get/<int:id>', views.get_holiday_template_details, name='get_holiday_template_details'),
    path('create', views.create_holiday_template_details, name='create_holiday_template_details'),
    path('update/<int:id>', views.update_holiday_template_details, name='update_holiday_template_details'),
    path('delete/<int:id>', views.delete_holiday_template_details, name='delete_holiday_template_details'),
]

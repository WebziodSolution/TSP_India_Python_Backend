from django.urls import path
from . import views

urlpatterns = [
    path('get/all/<int:id>', views.get_all_company_theme, name='get_all_company_theme'),
    path('get/<int:id>', views.get_company_theme, name='get_company_theme'),
    path('create', views.create_company_theme, name='create_company_theme'),
    path('update/<int:id>', views.update_company_theme, name='update_company_theme'),
    path('delete/<int:id>', views.delete_company_theme, name='delete_company_theme'),
]

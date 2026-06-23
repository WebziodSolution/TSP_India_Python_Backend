from django.urls import path
from . import views

urlpatterns = [
    path('getAllStatementMasters/<str:id>', views.get_all_statement_masters, name='get_all_statement_masters'),
    path('getAllStatementMasters', views.get_statement_masters_by_month_and_year, name='get_statement_masters_by_month_and_year'),
    path('get/<str:id>', views.get_salary_statement_master_by_id, name='get_salary_statement_master_by_id'),
    path('create', views.create_salary_statement_master, name='create_salary_statement_master'),
    path('update/<str:id>', views.update_salary_statement_master, name='update_salary_statement_master'),
    path('delete/<str:id>', views.delete_salary_statement_master, name='delete_salary_statement_master'),
]

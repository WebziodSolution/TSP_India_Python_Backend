from django.urls import path
from . import views

urlpatterns = [
    path('getEmployeeSalaryStatements', views.get_employee_salary_statements, name='get_employee_salary_statements'),
]

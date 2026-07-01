from django.urls import path
from . import views

urlpatterns = [
    path('get/all/<int:companyId>', views.get_all_employee_leave_masters, name='get_all_employee_leave_masters'),
    path('get/employee/<int:employeeId>', views.get_employee_leave_masters_by_employee, name='get_employee_leave_masters_by_employee'),
    path('get/<int:id>', views.get_employee_leave_master, name='get_employee_leave_master'),
    path('create', views.create_employee_leave_master, name='create_employee_leave_master'),
    path('update/<int:id>', views.update_employee_leave_master, name='update_employee_leave_master'),
    path('delete/<int:id>', views.delete_employee_leave_master, name='delete_employee_leave_master'),
]

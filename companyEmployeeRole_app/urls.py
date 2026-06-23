from django.urls import path
from . import views

urlpatterns = [
    path('getAllRoleList', views.get_all_roles_list, name='get_all_roles_list'),
    path('rolesListPage', views.roles_list, name='roles_list'),
    path('getAllRoles', views.get_all_roles, name='get_all_roles'),
    path('getActions/<int:roleId>', views.get_actions, name='get_actions'),
    path('getAllCompanyEmployeeRoles/<int:id>', views.get_all_company_employee_roles, name='get_all_company_employee_roles'),
    path('get/<int:id>', views.get_employee_roles, name='get_employee_roles'),
    path('create', views.create_employee_roles, name='create_employee_roles'),
    path('update/<int:id>', views.update_employee_roles, name='update_employee_roles'),
    path('delete/<int:id>', views.delete_employee_roles, name='delete_employee_roles'),
]

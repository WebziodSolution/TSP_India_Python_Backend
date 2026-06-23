from django.urls import path
from . import views

urlpatterns = [
    path('getAllRoleList', views.get_all_roles_list, name='get_all_roles_list'),
    path('create', views.create_role, name='create_role'),
    path('rolesListPage', views.roles_list, name='roles_list'),
    path('getAllRoles', views.get_all_roles, name='get_all_roles'),
    path('get/<str:roleId>', views.get_role_by_id, name='get_role_by_id'),
    path('update/<str:roleId>', views.update_role_by_id, name='update_role_by_id'),
    path('delete/<str:roleId>', views.delete_role_by_id, name='delete_role_by_id'),
    path('getActions/<str:roleId>', views.get_actions, name='get_actions'),
]

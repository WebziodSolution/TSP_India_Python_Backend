from django.urls import path
from . import views

urlpatterns = [
    path('create', views.create_module, name='create_module'),
    path('allModuleListPage', views.all_module_list_page, name='all_module_list_page'),
    path('moduleByFunctionalityListPage', views.module_by_functionality_list_page, name='module_by_functionality_list_page'),
    path('getAllModules', views.get_all_modules, name='get_all_modules'),
    path('get/<str:moduleId>', views.get_module_by_id, name='get_module_by_id'),
    path('update/<str:moduleId>', views.update_module_by_id, name='update_module_by_id'),
    path('delete/<str:moduleId>', views.delete_module_by_id, name='delete_module_by_id'),
]

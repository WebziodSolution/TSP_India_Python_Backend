from django.urls import path
from . import views

urlpatterns = [
    path('get/all/<str:flag>/<str:companyId>', views.get_all_by_company_id, name='get_all_by_company_id'),
    path('get/<str:id>', views.get_by_id, name='get_by_id'),
    path('create', views.create, name='create'),
    path('update/<str:id>', views.update, name='update'),
    path('delete/<str:id>', views.delete, name='delete'),
]

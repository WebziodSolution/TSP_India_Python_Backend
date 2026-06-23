from django.urls import path
from . import views

urlpatterns = [
    path('getAllHistory', views.filter_salary_statement_history, name='filter_salary_statement_history'),
    path('getHistory/<str:id>', views.get_salary_statement_history, name='get_salary_statement_history'),
    path('addHistory', views.add_salary_statement, name='add_salary_statement'),
    path('updateHistory/<str:id>', views.update_salary_statement, name='update_salary_statement'),
    path('deleteHistory/<str:id>', views.delete_salary_statement, name='delete_salary_statement'),
]

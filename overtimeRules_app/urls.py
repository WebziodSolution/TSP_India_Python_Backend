from django.urls import path
from . import views

urlpatterns = [
    path('getAllOvertimeRules/<str:id>', views.get_all_overtime_rules, name='get_all_overtime_rules'),
    path('getOvertimeRule/<str:id>', views.get_overtime_rule, name='get_overtime_rule'),
    path('createOvertimeRule/<str:id>', views.create_overtime_rule, name='create_overtime_rule'),
    path('updateOvertimeRule/<str:id>', views.update_overtime_rule, name='update_overtime_rule'),
    path('deleteOvertimeRule/<str:id>', views.delete_overtime_rule, name='delete_overtime_rule'),
]

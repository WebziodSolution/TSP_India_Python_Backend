from django.urls import path
from . import views

urlpatterns = [
    path('inoutreport', views.get_report, name='get_report'),
    path('generateExcelReport', views.generate_excel_report, name='generate_excel_report'),
    path('getDashboardData/<str:companyId>', views.get_dashboard_data, name='get_dashboard_data'),
    path('getUserLastInOut/<str:userId>', views.get_user_last_inout, name='get_user_last_inout'),
    path('getAllRecords', views.get_all_records, name='get_all_records'),
    path('getAllRecordsGroupByUser', views.get_all_records_grouped_by_user, name='get_all_records_grouped_by_user'),
    path('todayrecords', views.get_today_records, name='get_today_records'),
    path('get/<str:id>', views.get_user_inout, name='get_user_inout'),
    path('create', views.create_user_inout, name='create_user_inout'),
    path('update/<str:id>', views.update_user_inout_by_id, name='update_user_inout_by_id'),
    path('update', views.update_user_inout_by_dto, name='update_user_inout_by_dto'),
    path('clockInOut', views.clock_in_out, name='clock_in_out'),
    path('addClockInOut', views.add_clock_in_out, name='add_clock_in_out'),
    path('addBulk', views.add_bulk_clock_in_out, name='add_bulk_clock_in_out'),
    path('delete/<str:id>', views.delete_user_inout, name='delete_user_inout'),
]

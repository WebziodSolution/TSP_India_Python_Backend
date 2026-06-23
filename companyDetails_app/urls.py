from django.urls import path
from . import views

urlpatterns = [
    path('search', views.search, name='search_companies'),
    path('get/all', views.get_all_company_details, name='get_all_company_details'),
    path('get/<str:id>', views.get_company_details, name='get_company_details'),
    path('create/<str:step>', views.create_company_details, name='create_company_details'),
    path('update/<str:id>/<str:step>', views.update_company_details, name='update_company_details'),
    path('delete/<str:id>', views.delete_company_details, name='delete_company_details'),
    path('uploadCompanyLogo', views.upload_company_logo, name='upload_company_logo'),
    path('deleteCompanyLogo/<str:companyId>', views.delete_company_logo, name='delete_company_logo'),
    path('getLastCompany', views.get_last_company, name='get_last_company'),
    path('updateAutoTimeInAfterHours/<str:companyId>', views.update_auto_time_in_after_hours, name='update_auto_time_in_after_hours'),
    path('getAutoTimeInAfterHours/<str:companyId>', views.get_auto_time_in_after_hours, name='get_auto_time_in_after_hours'),
]

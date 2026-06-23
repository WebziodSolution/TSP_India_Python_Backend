from django.urls import path
from . import views

urlpatterns = [
    path('getAllCompanyEmployee/<int:companyId>', views.get_all_employee_by_company_id, name='get_all_employee_by_company_id'),
    path('getEmployeePFAndPTReport', views.get_employee_pf_and_pt_report, name='get_employee_pf_and_pt_report'),
    path('getAllEmployeeListByCompanyId/<int:companyId>', views.get_all_employee_list_by_company_id, name='get_all_employee_list_by_company_id'),
    path('get/<int:id>', views.get_employee, name='get_employee'),
    path('create', views.create_employee, name='create_employee'),
    path('update/<int:id>', views.update_employee, name='update_employee'),
    path('delete/<int:id>', views.delete_employee, name='delete_employee'),
    path('uploadEmployeeProfile', views.upload_employee_profile, name='upload_employee_profile'),
    path('deleteEmployeeImage/<int:companyId>/<int:employeeId>', views.delete_employee_image, name='delete_employee_image'),
    path('uploadEmployeeAadharImage', views.upload_employee_aadhar_image, name='upload_employee_aadhar_image'),
    path('deleteEmployeeAadharImage/<int:companyId>/<int:employeeId>', views.delete_employee_aadhar_image, name='delete_employee_aadhar_image'),
    path('createEmployee', views.create_employee_from_tsp, name='create_employee_from_tsp'),
    path('updateEmployee/<int:id>', views.update_employee_from_tsp, name='update_employee_from_tsp'),
    path('getLastUserId', views.get_last_user_id, name='get_last_user_id'),
]

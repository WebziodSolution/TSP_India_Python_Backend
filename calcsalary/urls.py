"""
URL configuration for calcsalary project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path('', include('common.urls')),
    path('user/', include('users_app.urls')),
    path('companyDetails/', include('companyDetails_app.urls')),
    path('companyActions/', include('companyAction_app.urls')),
    path('companyFunctionality/', include('companyFunctionality_app.urls')),
    path('companyModule/', include('companyModule_app.urls')),
    path('companyRoleActions/', include('companyRoleActions_app.urls')),
    path('employeeRole/', include('companyEmployeeRole_app.urls')),
    path('companyShift/', include('companyShift_app.urls')),
    path('companyTheme/', include('companyTheme_app.urls')),
    path('contractor/', include('contractor_app.urls')),
    path('country/', include('country_app.urls')),
    path('state/', include('countryToState_app.urls')),
    path('deductions/', include('deductions_app.urls')),
    path('department/', include('department_app.urls')),
    path('employeeBankInfo/', include('employeeBackAccountInfo_app.urls')),
    path('employeeType/', include('employeeType_app.urls')),
    path('employmentInfo/', include('employmentInfo_app.urls')),
    path('holidayTemplates/', include('holidayTemplates_app.urls')),
    path('holidayTemplateDetails/', include('holidayTemplateDetails_app.urls')),
    path('location/', include('locations_app.urls')),
    path('overtimerules/', include('overtimeRules_app.urls')),
    path('attendancePenaltyRules/', include('attendancePenaltyRules_app.urls')),
    path('usershift/', include('userShift_app.urls')),
    path('weekly-off/', include('weeklyOff_app.urls')),
    path('actions/', include('actions_app.urls')),
    path('functionality/', include('functionality_app.urls')),
    path('module/', include('module_app.urls')),
    path('roles/', include('roles_app.urls')),
    path('companyReport/', include('companyReport_app.urls')),
    path('inout/', include('userInOut_app.urls')),
    path('salaryStatementHistory/', include('salaryStatementHistory_app.urls')),
    path('statementMaster/', include('salaryStatementMaster_app.urls')),
    path('companyEmployee/', include('companyEmployee_app.urls')),
    path('employee/statement/', include('employeeStatements_app.urls')),
    # Swagger API Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]


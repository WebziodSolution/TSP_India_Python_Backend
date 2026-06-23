from django.db import models

class CompanyEmployeeRoles(models.Model):
    roleId = models.AutoField(primary_key=True, db_column='id')
    companyDetails = models.ForeignKey('CompanyDetails', on_delete=models.CASCADE, db_column='company_id', related_name='+')
    roleName = models.CharField(max_length=255, null=True, blank=True, db_column='role_name')

    class Meta:
        db_table = 'company_employee_roles'
        app_label = 'common'

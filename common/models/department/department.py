from django.db import models

class Department(models.Model):
    id = models.BigAutoField(primary_key=True, db_column='id')
    departmentName = models.CharField(max_length=255, db_column='department_name')
    companyDetails = models.ForeignKey('CompanyDetails', on_delete=models.CASCADE, db_column='company_id', null=True, blank=True, related_name='+')

    class Meta:
        db_table = 'departments'
        app_label = 'common'

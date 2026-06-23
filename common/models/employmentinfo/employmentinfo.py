from django.db import models

class EmploymentInfo(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    workPhone = models.CharField(max_length=255, null=True, blank=True, db_column='work_phone')
    ext = models.CharField(max_length=255, null=True, blank=True)
    workEmail = models.CharField(max_length=255, null=True, blank=True, db_column='work_email')
    hireDate = models.DateTimeField(null=True, blank=True, db_column='hire_date')
    status = models.CharField(max_length=255, null=True, blank=True)
    paidPension = models.CharField(max_length=255, null=True, blank=True, db_column='paid_pension')
    statutoryEmployee = models.CharField(max_length=255, null=True, blank=True, db_column='statutory_employee')
    exclusionIndicator = models.CharField(max_length=255, null=True, blank=True, db_column='exclusion_indicator')
    keyEmployeeIndicator = models.CharField(max_length=255, null=True, blank=True, db_column='key_employee_indicator')
    unionIndicator = models.CharField(max_length=255, null=True, blank=True, db_column='union_indicator')
    hce = models.CharField(max_length=255, null=True, blank=True)
    eligibilityIndicator = models.CharField(max_length=255, null=True, blank=True, db_column='eligibility_indicator')
    companyEmployee = models.ForeignKey('CompanyEmployee', on_delete=models.CASCADE, db_column='employee_id', null=True, blank=True, related_name='+')

    class Meta:
        db_table = 'employment_info'
        app_label = 'common'

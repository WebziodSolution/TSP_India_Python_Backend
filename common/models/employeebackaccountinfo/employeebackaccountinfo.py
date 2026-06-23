from django.db import models

class EmployeeBackAccountInfo(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    accountType = models.CharField(max_length=255, null=True, blank=True, db_column='account_type')
    ifscCode = models.CharField(max_length=255, null=True, blank=True, db_column='ifsc_code')
    branch = models.CharField(max_length=255, null=True, blank=True)
    bankName = models.CharField(max_length=255, null=True, blank=True, db_column='bank_name')
    accountNumber = models.CharField(max_length=255, null=True, blank=True, db_column='account_number')
    address = models.CharField(max_length=255, null=True, blank=True)
    passbookImage = models.CharField(max_length=255, null=True, blank=True, db_column='passbook_image')
    companyEmployee = models.ForeignKey('CompanyEmployee', on_delete=models.CASCADE, db_column='employee_id', null=True, blank=True, related_name='+')

    class Meta:
        db_table = 'employee_backaccount_info'
        app_label = 'common'

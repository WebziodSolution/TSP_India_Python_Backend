from django.db import models

class Deductions(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    companyEmployee = models.ForeignKey('CompanyEmployee', on_delete=models.CASCADE, db_column='employee_id', related_name='+')
    type = models.CharField(max_length=250, null=True, blank=True)
    label = models.CharField(max_length=250, null=True, blank=True)
    amount = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'deductions'
        app_label = 'common'

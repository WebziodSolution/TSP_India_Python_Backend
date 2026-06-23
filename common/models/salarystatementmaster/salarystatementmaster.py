from django.db import models

class SalaryStatementMaster(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    companyDetails = models.ForeignKey('CompanyDetails', on_delete=models.CASCADE, db_column='company_id', null=True, blank=True, related_name='+')
    month = models.IntegerField(null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)
    totalSalary = models.IntegerField(null=True, blank=True, db_column='total_salary')
    totalPf = models.IntegerField(null=True, blank=True, db_column='total_pf')
    totalPt = models.IntegerField(null=True, blank=True, db_column='total_pt')
    note = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'salary_statement_master'
        app_label = 'common'

from django.db import models

class SalaryStatementHistory(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    companyDetails = models.ForeignKey('CompanyDetails', on_delete=models.CASCADE, db_column='company_id', related_name='+')
    clockInOutId = models.IntegerField(null=True, blank=True, db_column='clock_in_out_id')
    employeeId = models.IntegerField(null=True, blank=True, db_column='employee_id')
    employeeName = models.CharField(max_length=255, null=True, blank=True, db_column='employee_name')
    departmentId = models.IntegerField(null=True, blank=True, db_column='department_id')
    departmentName = models.CharField(max_length=255, null=True, blank=True, db_column='department_name')
    basicSalary = models.IntegerField(null=True, blank=True, db_column='basic_salary')
    totalEarnSalary = models.IntegerField(null=True, blank=True, db_column='total_earn_salary')
    otAmount = models.IntegerField(null=True, blank=True, db_column='ot_amount')
    pfAmount = models.IntegerField(null=True, blank=True, db_column='pf_amount')
    pfPercentage = models.IntegerField(null=True, blank=True, db_column='pf_percentage')
    totalPfAmount = models.IntegerField(null=True, blank=True, db_column='total_pf_amount')
    ptAmount = models.IntegerField(null=True, blank=True, db_column='pt_amount')
    totalEarnings = models.IntegerField(null=True, blank=True, db_column='total_earnings')
    totalDeductions = models.IntegerField(null=True, blank=True, db_column='total_deductions')
    totalPenaltyAmount = models.IntegerField(null=True, blank=True, db_column='total_penalty_amount')
    otherDeductions = models.IntegerField(null=True, blank=True, db_column='other_deductions')
    netSalary = models.IntegerField(null=True, blank=True, db_column='net_salary')
    monthYear = models.CharField(max_length=255, null=True, blank=True, db_column='salary_month_and_year')
    month = models.IntegerField(null=True, blank=True, db_column='salary_month')
    year = models.IntegerField(null=True, blank=True, db_column='salary_year')
    totalPaidDays = models.IntegerField(null=True, blank=True, db_column='total_paid_days')
    totalWorkingDays = models.IntegerField(null=True, blank=True, db_column='working_days')
    totalWorkingHours = models.FloatField(null=True, blank=True, db_column='working_hours')
    totalDays = models.IntegerField(null=True, blank=True, db_column='total_days')
    note = models.CharField(max_length=255, null=True, blank=True)
    companyEmployee = models.ForeignKey('CompanyEmployee', on_delete=models.SET_NULL, db_column='generated_by', null=True, blank=True, related_name='+')
    generatedDate = models.DateField(null=True, blank=True, db_column='generated_date')

    class Meta:
        db_table = 'salary_statement_history'
        app_label = 'common'

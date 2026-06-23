from django.db import models

class AttendancePenaltyRules(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    ruleName = models.CharField(max_length=255, null=True, blank=True, db_column='rule_name')
    companyDetails = models.ForeignKey('CompanyDetails', on_delete=models.CASCADE, db_column='company_id', null=True, blank=True, related_name='+')
    companyEmployee = models.ForeignKey('CompanyEmployee', on_delete=models.SET_NULL, db_column='created_by', null=True, blank=True, related_name='+')
    minutes = models.IntegerField(null=True, blank=True)
    deductionType = models.CharField(max_length=255, null=True, blank=True, db_column='deduction_type')
    amount = models.IntegerField(null=True, blank=True)
    count = models.IntegerField(null=True, blank=True)
    isEarlyExit = models.BooleanField(default=False, null=True, blank=True, db_column='is_early_exit')

    class Meta:
        db_table = 'attendance_penalty_rules'
        app_label = 'common'

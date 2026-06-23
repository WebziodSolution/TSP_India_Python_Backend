from django.db import models

class OvertimeRules(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    companyDetails = models.ForeignKey('CompanyDetails', on_delete=models.CASCADE, db_column='company_id', null=True, blank=True, related_name='+')
    companyEmployee = models.ForeignKey('CompanyEmployee', on_delete=models.SET_NULL, db_column='created_by', null=True, blank=True, related_name='+')
    ruleName = models.CharField(max_length=255, null=True, blank=True, db_column='rule_name')
    otMinutes = models.IntegerField(null=True, blank=True, db_column='ot_minutes')
    otAmount = models.FloatField(null=True, blank=True, db_column='ot_amount')
    otType = models.CharField(max_length=255, null=True, blank=True, db_column='ot_type')

    class Meta:
        db_table = 'overtime_rules'
        app_label = 'common'

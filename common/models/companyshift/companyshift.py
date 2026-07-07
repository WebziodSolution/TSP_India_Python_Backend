from django.db import models

class CompanyShift(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    companyDetails = models.ForeignKey('CompanyDetails', on_delete=models.CASCADE, db_column='company_id', null=True, blank=True, related_name='+')
    shiftName = models.CharField(max_length=255, null=True, blank=True, db_column='shift_name')
    shiftType = models.CharField(max_length=255, null=True, blank=True, db_column='shift_type')
    startTime = models.DateTimeField(null=True, blank=True, db_column='time_start')
    endTime = models.DateTimeField(null=True, blank=True, db_column='time_end')
    hours = models.FloatField(null=True, blank=True)
    totalHours = models.FloatField(null=True, blank=True, db_column='total_hours')

    class Meta:
        db_table = 'company_shift'
        app_label = 'common'

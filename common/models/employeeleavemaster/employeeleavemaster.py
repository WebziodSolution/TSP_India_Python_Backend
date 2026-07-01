from django.db import models

class EmployeeLeaveMaster(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')    
    companyEmployee = models.ForeignKey('CompanyEmployee', on_delete=models.SET_NULL, db_column='employee_id', null=True, blank=True, related_name='+')
    leaveType = models.ForeignKey('LeaveType', on_delete=models.SET_NULL, db_column='leave_type_id', null=True, blank=True, related_name='+')
    totalLeave = models.IntegerField(db_column='total_leave', null=True, blank=True)
    usedLeave = models.IntegerField(db_column='used_leave', null=True, blank=True)
    class Meta:
        db_table = 'employee_leave_master'
        app_label = 'common'

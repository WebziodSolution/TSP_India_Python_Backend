from django.db import models

class UserInOut(models.Model):
    id = models.BigAutoField(primary_key=True, db_column='id')
    timeIn = models.DateTimeField(null=True, blank=True, db_column='time_in')
    timeOut = models.DateTimeField(null=True, blank=True, db_column='time_out')
    createdOn = models.DateTimeField(null=True, blank=True, db_column='created_on')
    user = models.ForeignKey('CompanyEmployee', on_delete=models.CASCADE, db_column='user_id', null=True, blank=True, related_name='+')
    locations = models.ForeignKey('Locations', on_delete=models.CASCADE, db_column='location_id', null=True, blank=True, related_name='+')
    companyDetails = models.ForeignKey('CompanyDetails', on_delete=models.CASCADE, db_column='company_id', null=True, blank=True, related_name='+')
    isSalaryGenerate = models.IntegerField(null=True, blank=True, db_column='is_salary_generate')

    class Meta:
        db_table = 'user_inout'
        app_label = 'common'

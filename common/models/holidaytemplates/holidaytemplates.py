from django.db import models

class HolidayTemplates(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    name = models.CharField(max_length=255)
    companyDetails = models.ForeignKey('CompanyDetails', on_delete=models.CASCADE, db_column='company_id', null=True, blank=True, related_name='+')
    companyEmployee = models.ForeignKey('CompanyEmployee', on_delete=models.SET_NULL, db_column='created_by', null=True, blank=True, related_name='+')

    class Meta:
        db_table = 'holiday_templates'
        app_label = 'common'

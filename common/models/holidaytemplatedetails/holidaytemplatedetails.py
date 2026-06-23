from django.db import models

class HolidayTemplateDetails(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    name = models.CharField(max_length=255)
    date = models.DateField()
    holidayTemplates = models.ForeignKey('HolidayTemplates', on_delete=models.CASCADE, db_column='holiday_template_id', related_name='+')

    class Meta:
        db_table = 'holiday_template_details'
        app_label = 'common'

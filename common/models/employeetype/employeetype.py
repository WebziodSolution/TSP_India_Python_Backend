from django.db import models

class EmployeeType(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    name = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'employee_type'
        app_label = 'common'

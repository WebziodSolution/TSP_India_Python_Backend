from django.db import models

class Contractor(models.Model):
    id = models.BigAutoField(primary_key=True, db_column='id')
    contractorName = models.CharField(max_length=255, null=True, blank=True, db_column='contractor_name')

    class Meta:
        db_table = 'contractor'
        app_label = 'common'

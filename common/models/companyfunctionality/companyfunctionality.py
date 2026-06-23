from django.db import models

class CompanyFunctionality(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    functionalityName = models.CharField(max_length=255, db_column='functionality_name')

    class Meta:
        db_table = 'company_functionality'
        app_label = 'common'

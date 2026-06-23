from django.db import models

class CompanyModules(models.Model):
    moduleId = models.AutoField(primary_key=True, db_column='id')
    moduleName = models.CharField(max_length=255, null=True, blank=True, db_column='module_name')
    functionality = models.ForeignKey('CompanyFunctionality', on_delete=models.CASCADE, db_column='functionality_id', null=True, blank=True, related_name='+')

    class Meta:
        db_table = 'company_modules'
        app_label = 'common'

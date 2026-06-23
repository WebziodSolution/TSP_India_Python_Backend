from django.db import models

class Module(models.Model):
    moduleId = models.BigAutoField(primary_key=True, db_column='module_Id')
    moduleName = models.CharField(max_length=255, null=True, blank=True, db_column='module_name')
    functionality = models.ForeignKey('Functionality', on_delete=models.SET_NULL, db_column='functionality_id', null=True, blank=True, related_name='+')

    class Meta:
        db_table = 'module'
        app_label = 'common'

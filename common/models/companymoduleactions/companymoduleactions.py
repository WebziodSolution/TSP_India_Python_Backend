from django.db import models

class CompanyModuleActions(models.Model):
    moduleActionId = models.AutoField(primary_key=True, db_column='id')
    module = models.ForeignKey('CompanyModules', on_delete=models.CASCADE, db_column='module_id', related_name='+')
    action = models.ForeignKey('CompanyActions', on_delete=models.CASCADE, db_column='action_id', null=True, blank=True, related_name='+')

    class Meta:
        db_table = 'company_module_actions'
        app_label = 'common'

from django.db import models

class ModuleActions(models.Model):
    moduleActionId = models.BigAutoField(primary_key=True, db_column='module_action_Id')
    module = models.ForeignKey('Module', on_delete=models.CASCADE, db_column='module_id', null=True, blank=True, related_name='+')
    action = models.ForeignKey('Actions', on_delete=models.CASCADE, db_column='action_id', null=True, blank=True, related_name='+')
    # roleModuleActions = models.CharField(max_length=255, null=True, blank=True, db_column='role_module_actions')

    class Meta:
        db_table = 'module_actions'
        app_label = 'common'

from django.db import models

class RoleModuleActions(models.Model):
    roleActionId = models.BigAutoField(primary_key=True, db_column='role_action_Id')
    role = models.ForeignKey('Roles', on_delete=models.CASCADE, db_column='role_id', null=True, blank=True, related_name='+')
    moduleActions = models.ForeignKey('ModuleActions', on_delete=models.CASCADE, db_column='module_action_Id', null=True, blank=True, related_name='+')

    class Meta:
        db_table = 'role_module_actions'
        app_label = 'common'

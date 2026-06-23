from django.db import models

class CompanyRoleModuleActions(models.Model):
    roleActionId = models.AutoField(primary_key=True, db_column='id')
    role = models.ForeignKey('CompanyEmployeeRoles', on_delete=models.CASCADE, db_column='role_id', null=True, blank=True, related_name='+')
    moduleActions = models.ForeignKey('CompanyModuleActions', on_delete=models.CASCADE, db_column='module_action_Id', null=True, blank=True, related_name='+')

    class Meta:
        db_table = 'company_role_module_actions'
        app_label = 'common'

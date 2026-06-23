from django.db import models

class Roles(models.Model):
    roleId = models.BigAutoField(primary_key=True, db_column='role_Id')
    roleName = models.CharField(max_length=255, null=True, blank=True, db_column='role_name')

    class Meta:
        db_table = 'roles'
        app_label = 'common'

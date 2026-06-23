from django.db import models

class CompanyActions(models.Model):
    actionId = models.AutoField(primary_key=True, db_column='id')
    actionName = models.CharField(max_length=255, null=True, blank=True, db_column='action_name')

    class Meta:
        db_table = 'company_actions'
        app_label = 'common'

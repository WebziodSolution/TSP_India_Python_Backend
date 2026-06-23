from django.db import models

class Actions(models.Model):
    actionId = models.BigAutoField(primary_key=True, db_column='action_Id')
    actionName = models.CharField(max_length=255, null=True, blank=True, db_column='action_name')

    class Meta:
        db_table = 'actions'
        app_label = 'common'

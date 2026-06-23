from django.db import models

class Functionality(models.Model):
    id = models.BigAutoField(primary_key=True, db_column='id')
    functionalityName = models.CharField(max_length=255, db_column='functionality_name')

    class Meta:
        db_table = 'functionality'
        app_label = 'common'

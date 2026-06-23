from django.db import models

class UserShift(models.Model):
    id = models.BigAutoField(primary_key=True, db_column='id')
    shiftName = models.CharField(max_length=255, null=True, blank=True, db_column='shift_name')

    class Meta:
        db_table = 'user_shift'
        app_label = 'common'

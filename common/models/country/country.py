from django.db import models

class Country(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    iso2 = models.CharField(max_length=2, null=True, blank=True)
    cntName = models.CharField(max_length=255, null=True, blank=True, db_column='cnt_name')
    longName = models.CharField(max_length=255, null=True, blank=True, db_column='long_name')
    oid = models.IntegerField(null=True, blank=True)
    cntCode = models.CharField(max_length=255, null=True, blank=True, db_column='cnt_code')
    phoneMinLength = models.IntegerField(null=True, blank=True, db_column='phone_min_length')
    phoneMaxLength = models.IntegerField(null=True, blank=True, db_column='phone_max_length')

    class Meta:
        db_table = 'tbl_country'
        app_label = 'common'

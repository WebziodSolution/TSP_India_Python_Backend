from django.db import models

class CountryToState(models.Model):
    id = models.AutoField(primary_key=True, db_column='country_to_state_id')
    country = models.ForeignKey('Country', on_delete=models.SET_NULL, db_column='fk_country_id', null=True, blank=True, related_name='+')
    stateCapital = models.CharField(max_length=100, null=True, blank=True, db_column='state_capital')
    stateLong = models.CharField(max_length=100, null=True, blank=True, db_column='state_long')
    stateShort = models.CharField(max_length=10, null=True, blank=True, db_column='state_short')

    class Meta:
        db_table = 'country_to_state'
        app_label = 'common'
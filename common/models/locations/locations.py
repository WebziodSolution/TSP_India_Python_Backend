from django.db import models

class Locations(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    locationName = models.CharField(max_length=255, null=True, blank=True, db_column='location_name')
    city = models.CharField(max_length=255, null=True, blank=True, db_column='city')
    state = models.CharField(max_length=255, null=True, blank=True, db_column='state')
    country = models.CharField(max_length=255, null=True, blank=True, db_column='country')
    address1 = models.CharField(max_length=255, null=True, blank=True, db_column='address1')
    address2 = models.CharField(max_length=255, null=True, blank=True, db_column='address2')
    zipCode = models.CharField(max_length=255, null=True, blank=True, db_column='zip_code')
    employeeCount = models.CharField(max_length=255, null=True, blank=True, db_column='employee_count')
    externalId = models.CharField(max_length=255, null=True, blank=True, db_column='radar_external_id')
    geofenceId = models.CharField(max_length=255, null=True, blank=True, db_column='geofence_Id')
    isActive = models.IntegerField(null=True, blank=True, db_column='is_active')
    payPeriod = models.IntegerField(null=True, blank=True, db_column='pay_period')
    payPeriodStart = models.DateField(null=True, blank=True, db_column='pay_period_start')
    payPeriodEnd = models.DateField(null=True, blank=True, db_column='pay_period_end')
    companyDetails = models.ForeignKey('CompanyDetails', on_delete=models.CASCADE, db_column='company_id', null=True, blank=True, related_name='+')

    class Meta:
        db_table = 'locations'
        app_label = 'common'

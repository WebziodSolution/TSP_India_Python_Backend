from django.db import models

class CompanyDetails(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    companyNo = models.CharField(max_length=255, null=True, blank=True, db_column='company_no')
    companyName = models.CharField(max_length=255, null=True, blank=True, db_column='company_name')
    dba = models.CharField(max_length=255, null=True, blank=True, db_column='DBA')
    companyLogo = models.CharField(max_length=255, null=True, blank=True, db_column='company_logo')
    email = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    industryName = models.CharField(max_length=255, null=True, blank=True, db_column='industry_name')
    websiteUrl = models.CharField(max_length=255, null=True, blank=True, db_column='website_url')
    isActive = models.IntegerField(null=True, blank=True, db_column='is_active')
    registerDate = models.DateTimeField(null=True, blank=True, db_column='register_date')
    ein = models.CharField(max_length=255, null=True, blank=True, db_column='EIN')
    organizationType = models.CharField(max_length=255, null=True, blank=True, db_column='organization_type')
    # companyEmployees = models.CharField(max_length=255, null=True, blank=True, db_column='company_employees')
    autoTimeInAfterHours = models.CharField(max_length=255, null=True, blank=True, db_column='auto_time_in_after_hours')

    class Meta:
        db_table = 'company_details'
        app_label = 'common'

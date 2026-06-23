from django.db import models

class CompanyTheme(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    companyDetails = models.ForeignKey('CompanyDetails', on_delete=models.CASCADE, db_column='company_id', null=True, blank=True, related_name='+')
    primaryColor = models.CharField(max_length=255, null=True, blank=True, db_column='primary_color')
    sideNavigationBgColor = models.CharField(max_length=255, null=True, blank=True, db_column='side_navigation_bg_color')
    contentBgColor = models.CharField(max_length=255, null=True, blank=True, db_column='content_bg_color')
    contentBgColor2 = models.CharField(max_length=255, null=True, blank=True, db_column='content_bg_color2')
    headerBgColor = models.CharField(max_length=255, null=True, blank=True, db_column='header_bg_color')
    textColor = models.CharField(max_length=255, null=True, blank=True, db_column='text_color')
    iconColor = models.CharField(max_length=255, null=True, blank=True, db_column='icon_color')

    class Meta:
        db_table = 'company_theme'
        app_label = 'common'

from rest_framework import serializers

class CompanyThemeSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False, allow_null=True)
    companyId = serializers.IntegerField(required=False, allow_null=True)
    primaryColor = serializers.CharField(required=False, allow_null=True)
    sideNavigationBgColor = serializers.CharField(required=False, allow_null=True)
    contentBgColor = serializers.CharField(required=False, allow_null=True)
    contentBgColor2 = serializers.CharField(required=False, allow_null=True)
    headerBgColor = serializers.CharField(required=False, allow_null=True)
    textColor = serializers.CharField(required=False, allow_null=True)
    iconColor = serializers.CharField(required=False, allow_null=True)
    type = serializers.CharField(required=False, allow_null=True)

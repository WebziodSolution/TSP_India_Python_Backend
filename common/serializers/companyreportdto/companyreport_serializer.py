from rest_framework import serializers

class CompanyReportSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False, allow_null=True)
    companyName = serializers.CharField(required=False, allow_null=True)
    email = serializers.CharField(required=False, allow_null=True)
    phone = serializers.CharField(required=False, allow_null=True)
    registerDate = serializers.CharField(required=False, allow_null=True)
    employeeCount = serializers.IntegerField(required=False, allow_null=True)

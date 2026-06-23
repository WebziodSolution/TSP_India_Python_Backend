from rest_framework import serializers

class SalaryStatementRequestSerializer(serializers.Serializer):
    employeeIds = serializers.JSONField(required=False, allow_null=True)
    departmentIds = serializers.JSONField(required=False, allow_null=True)
    month = serializers.IntegerField(required=False, allow_null=True)
    year = serializers.IntegerField(required=False, allow_null=True)
    companyId = serializers.IntegerField(required=False, allow_null=True)
    startDate = serializers.CharField(required=False, allow_null=True)
    endDate = serializers.CharField(required=False, allow_null=True)
    timeZone = serializers.CharField(required=False, allow_null=True)

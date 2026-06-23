from rest_framework import serializers

class EmploymentInfoSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False, allow_null=True)
    workPhone = serializers.CharField(required=False, allow_null=True)
    ext = serializers.CharField(required=False, allow_null=True)
    workEmail = serializers.CharField(required=False, allow_null=True)
    hireDate = serializers.CharField(required=False, allow_null=True)
    status = serializers.CharField(required=False, allow_null=True)
    paidPension = serializers.CharField(required=False, allow_null=True)
    statutoryEmployee = serializers.CharField(required=False, allow_null=True)
    exclusionIndicator = serializers.CharField(required=False, allow_null=True)
    keyEmployeeIndicator = serializers.CharField(required=False, allow_null=True)
    hce = serializers.CharField(required=False, allow_null=True)
    unionIndicator = serializers.CharField(required=False, allow_null=True)
    eligibilityIndicator = serializers.CharField(required=False, allow_null=True)
    employeeId = serializers.IntegerField(required=False, allow_null=True)

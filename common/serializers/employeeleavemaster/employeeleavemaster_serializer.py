from rest_framework import serializers

class EmployeeleavemasterSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False, allow_null=True)
    employeeId = serializers.IntegerField(required=False, allow_null=True)
    leaveTypeId = serializers.IntegerField(required=False, allow_null=True)
    totalLeave = serializers.IntegerField(required=False, allow_null=True)
    usedLeave = serializers.IntegerField(required=False, allow_null=True)
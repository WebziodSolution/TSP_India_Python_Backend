from rest_framework import serializers

class UserInOutSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False, allow_null=True)
    timeIn = serializers.CharField(required=False, allow_null=True)
    timeOut = serializers.CharField(required=False, allow_null=True)
    userId = serializers.IntegerField(required=False, allow_null=True)
    hourlyRate = serializers.FloatField(required=False, allow_null=True)
    userName = serializers.CharField(required=False, allow_null=True)
    firstName = serializers.CharField(required=False, allow_null=True)
    lastName = serializers.CharField(required=False, allow_null=True)
    createdOn = serializers.CharField(required=False, allow_null=True)
    locationId = serializers.IntegerField(required=False, allow_null=True)
    companyId = serializers.IntegerField(required=False, allow_null=True)
    companyShiftDto = serializers.JSONField(required=False, allow_null=True)  # Nested: CompanyShiftSerializer
    isSalaryGenerate = serializers.IntegerField(required=False, allow_null=True)
    timeZone = serializers.CharField(required=False, allow_null=True)
    regular = serializers.CharField(required=False, allow_null=True)
    breakTime = serializers.CharField(required=False, allow_null=True)
    overtime = serializers.CharField(required=False, allow_null=True)
    totalHours = serializers.CharField(required=False, allow_null=True)
    workHours = serializers.CharField(required=False, allow_null=True)
    status = serializers.CharField(required=False, allow_null=True)
    department = serializers.CharField(required=False, allow_null=True)

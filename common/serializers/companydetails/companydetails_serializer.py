from rest_framework import serializers

class CompanyDetailsSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False, allow_null=True)
    companyNo = serializers.CharField(required=True)
    companyName = serializers.CharField(required=True)
    dba = serializers.CharField(required=False, allow_null=True)
    companyLogo = serializers.CharField(required=False, allow_null=True)
    email = serializers.CharField(required=True)
    phone = serializers.CharField(required=True)
    industryName = serializers.CharField(required=False, allow_null=True)
    websiteUrl = serializers.CharField(required=False, allow_null=True)
    registerDate = serializers.CharField(required=False, allow_null=True)
    ein = serializers.CharField(required=False, allow_null=True)
    organizationType = serializers.CharField(required=False, allow_null=True)
    autoTimeInAfterHours = serializers.CharField(required=False, allow_null=True)
    locations = serializers.JSONField(required=False, allow_null=True)  # Nested: List<LocationDto>
    companyEmployeeDto = serializers.JSONField(required=False, allow_null=True)  # Nested: CompanyEmployeeSerializer
    employees = serializers.JSONField(required=False, allow_null=True)  # Nested: List<CompanyEmployeeDto>
    deletedEmployeeId = serializers.JSONField(required=False, allow_null=True)
    roles = serializers.JSONField(required=False, allow_null=True)  # Nested: List<CompanyEmployeeRolesDto>

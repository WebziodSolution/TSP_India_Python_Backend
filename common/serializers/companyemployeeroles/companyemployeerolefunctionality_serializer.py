from rest_framework import serializers

class CompanyEmployeeRoleFunctionalitySerializer(serializers.Serializer):
    functionalityId = serializers.IntegerField(required=False, allow_null=True)
    functionalityName = serializers.CharField(required=False, allow_null=True)
    modules = serializers.JSONField(required=False, allow_null=True)  # Nested: List<CompanyEmployeeRoleModuleDto>

from rest_framework import serializers

class CompanyEmployeeRolesActionsSerializer(serializers.Serializer):
    functionalities = serializers.JSONField(required=False, allow_null=True)  # Nested: List<CompanyEmployeeRoleFunctionalityDto>

from rest_framework import serializers

class RoleSerializer(serializers.Serializer):
    roleId = serializers.IntegerField(required=False, allow_null=True)
    roleName = serializers.CharField(required=False, allow_null=True)
    rolesActions = serializers.JSONField(required=False, allow_null=True)  # Nested: RolesActionsSerializer

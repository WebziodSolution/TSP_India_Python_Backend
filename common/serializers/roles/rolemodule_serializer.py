from rest_framework import serializers

class RoleModuleSerializer(serializers.Serializer):
    moduleId = serializers.IntegerField(required=False, allow_null=True)
    moduleName = serializers.CharField(required=False, allow_null=True)
    moduleAssignedActions = serializers.JSONField(required=False, allow_null=True)
    roleAssignedActions = serializers.JSONField(required=False, allow_null=True)

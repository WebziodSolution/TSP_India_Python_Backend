from rest_framework import serializers

class AssignActionsToModuleSerializer(serializers.Serializer):
    moduleId = serializers.IntegerField(required=False, allow_null=True)
    actionIds = serializers.JSONField(required=False, allow_null=True)

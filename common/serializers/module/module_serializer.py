from rest_framework import serializers

class ModuleSerializer(serializers.Serializer):
    moduleId = serializers.IntegerField(required=False, allow_null=True)
    moduleName = serializers.CharField(required=False, allow_null=True)
    functionalityId = serializers.IntegerField(required=False, allow_null=True)
    functionalityName = serializers.CharField(required=False, allow_null=True)
    actions = serializers.JSONField(required=False, allow_null=True)

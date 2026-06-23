from rest_framework import serializers

class FunctionalitySerializer(serializers.Serializer):
    functionalityId = serializers.IntegerField(required=False, allow_null=True)
    functionalityName = serializers.CharField(required=True)
    modules = serializers.JSONField(required=False, allow_null=True)  # Nested: List<RolesActionsDto>

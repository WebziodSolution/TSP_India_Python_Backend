from rest_framework import serializers

class RolesActionsSerializer(serializers.Serializer):
    functionalities = serializers.JSONField(required=False, allow_null=True)  # Nested: List<RoleFunctionalityDto>

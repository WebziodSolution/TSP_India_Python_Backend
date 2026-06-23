from rest_framework import serializers

class ActionSerializer(serializers.Serializer):
    actionId = serializers.IntegerField(required=False, allow_null=True)
    actionName = serializers.CharField(required=False, allow_null=True)

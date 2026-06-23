from rest_framework import serializers

class CompanyModuleActionsSerializer(serializers.Serializer):
    moduleActionId = serializers.IntegerField(required=False, allow_null=True)
    moduleId = serializers.IntegerField(required=False, allow_null=True)
    actionId = serializers.IntegerField(required=False, allow_null=True)

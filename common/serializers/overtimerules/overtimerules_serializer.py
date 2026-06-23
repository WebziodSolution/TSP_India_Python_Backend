from rest_framework import serializers

class OvertimeRulesSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False, allow_null=True)
    ruleName = serializers.CharField(required=False, allow_null=True)
    otMinutes = serializers.IntegerField(required=False, allow_null=True)
    otAmount = serializers.FloatField(required=False, allow_null=True)
    otType = serializers.CharField(required=False, allow_null=True)
    companyId = serializers.IntegerField(required=False, allow_null=True)
    createdBy = serializers.IntegerField(required=False, allow_null=True)
    createdByUserName = serializers.CharField(required=False, allow_null=True)

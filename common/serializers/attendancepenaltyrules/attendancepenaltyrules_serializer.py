from rest_framework import serializers

class AttendancePenaltyRulesSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False, allow_null=True)
    ruleName = serializers.CharField(required=False, allow_null=True)
    companyId = serializers.IntegerField(required=False, allow_null=True)
    createdBy = serializers.IntegerField(required=False, allow_null=True)
    createdByUserName = serializers.CharField(required=False, allow_null=True)
    minutes = serializers.IntegerField(required=False, allow_null=True)
    deductionType = serializers.CharField(required=False, allow_null=True)
    amount = serializers.IntegerField(required=False, allow_null=True)
    count = serializers.IntegerField(required=False, allow_null=True)
    isEarlyExit = serializers.BooleanField(default=False)

    def to_internal_value(self, data):
        data_copy = data.copy() if hasattr(data, 'copy') else dict(data)
        for field in ['count', 'amount', 'minutes', 'companyId', 'createdBy', 'id']:
            if field in data_copy and (data_copy[field] == "" or data_copy[field] == "null" or data_copy[field] is None):
                data_copy[field] = None
        return super().to_internal_value(data_copy)


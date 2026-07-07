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

    def to_internal_value(self, data):
        if hasattr(data, 'dict'):
            data = data.dict()
        else:
            data = dict(data)
        
        for field_name, field in self.fields.items():
            if not isinstance(field, serializers.CharField):
                if field_name in data and data[field_name] == "":
                    data[field_name] = None
                    
        return super().to_internal_value(data)

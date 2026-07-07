from rest_framework import serializers

class CompanyShiftSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False, allow_null=True)
    companyId = serializers.IntegerField(required=False, allow_null=True)
    shiftName = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    shiftType = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    startTime = serializers.DateTimeField(required=False, allow_null=True)
    endTime = serializers.DateTimeField(required=False, allow_null=True)
    hours = serializers.FloatField(required=False, allow_null=True)
    totalHours = serializers.FloatField(required=False, allow_null=True)

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

from rest_framework import serializers

class HolidayTemplateDetailsSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False, allow_null=True)
    name = serializers.CharField(required=False, allow_null=True)
    date = serializers.CharField(required=False, allow_null=True)
    holidayTemplateId = serializers.IntegerField(required=False, allow_null=True)

    def to_internal_value(self, data):
        data_copy = data.copy() if hasattr(data, 'copy') else dict(data)
        for field in ['id', 'holidayTemplateId']:
            if field in data_copy and (data_copy[field] == "" or data_copy[field] == "null" or data_copy[field] is None):
                data_copy[field] = None
        return super().to_internal_value(data_copy)


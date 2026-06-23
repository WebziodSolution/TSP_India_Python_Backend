from rest_framework import serializers

class HolidayTemplatesSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False, allow_null=True)
    name = serializers.CharField(required=False, allow_null=True)
    companyId = serializers.IntegerField(required=False, allow_null=True)
    createdBy = serializers.IntegerField(required=False, allow_null=True)
    createdByUserName = serializers.CharField(required=False, allow_null=True)
    holidayTemplateDetailsList = serializers.JSONField(required=False, allow_null=True)  # Nested: List<HolidayTemplateDetailsDto>
    assignedEmployeeIds = serializers.JSONField(required=False, allow_null=True)

    def to_internal_value(self, data):
        data_copy = data.copy() if hasattr(data, 'copy') else dict(data)
        for field in ['id', 'companyId', 'createdBy']:
            if field in data_copy and (data_copy[field] == "" or data_copy[field] == "null" or data_copy[field] is None):
                data_copy[field] = None
        return super().to_internal_value(data_copy)


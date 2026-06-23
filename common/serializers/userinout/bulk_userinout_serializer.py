from rest_framework import serializers

class BulkUserInOutSerializer(serializers.Serializer):
    userId = serializers.ListField(
        child=serializers.IntegerField(),
        required=True,
        allow_empty=False,
        error_messages={"required": "User ID list cannot be empty", "blank": "User ID list cannot be empty"}
    )
    startDate = serializers.CharField(required=True)
    endDate = serializers.CharField(required=True)
    timeIn = serializers.CharField(required=True)
    timeOut = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    companyId = serializers.IntegerField(required=True)

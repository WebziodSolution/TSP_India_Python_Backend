from rest_framework import serializers

class UserShiftSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False, allow_null=True)
    shiftName = serializers.CharField(required=False, allow_null=True)

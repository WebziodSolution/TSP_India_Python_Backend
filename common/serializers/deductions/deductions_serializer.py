from rest_framework import serializers

class DeductionsSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False, allow_null=True)
    employeeId = serializers.IntegerField(required=False, allow_null=True)
    type = serializers.CharField(required=False, allow_null=True)
    label = serializers.CharField(required=False, allow_null=True)
    amount = serializers.IntegerField(required=False, allow_null=True)

from rest_framework import serializers

class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(required=False, allow_null=True)
    currentPassword = serializers.CharField(required=False, allow_null=True)
    userId = serializers.CharField(required=False, allow_null=True)
    companyId = serializers.CharField(required=False, allow_null=True)
    token = serializers.CharField(required=False, allow_null=True)

from rest_framework import serializers

class LoginSerializer(serializers.Serializer):
    userName = serializers.CharField(required=True)
    companyId = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    noPassword = serializers.BooleanField(default=False)

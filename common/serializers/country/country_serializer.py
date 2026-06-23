from rest_framework import serializers

class CountrySerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False, allow_null=True)
    iso2 = serializers.CharField(required=False, allow_null=True)
    cntName = serializers.CharField(required=False, allow_null=True)
    longName = serializers.CharField(required=False, allow_null=True)
    oid = serializers.IntegerField(required=False, allow_null=True)
    cntCode = serializers.CharField(required=False, allow_null=True)
    phoneMinLength = serializers.IntegerField(required=False, allow_null=True)
    phoneMaxLength = serializers.IntegerField(required=False, allow_null=True)

from rest_framework import serializers

class CountryToStateSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False, allow_null=True)
    countryId = serializers.IntegerField(required=False, allow_null=True)
    stateLong = serializers.CharField(required=False, allow_null=True)
    stateShort = serializers.CharField(required=False, allow_null=True)
    stateCapital = serializers.CharField(required=False, allow_null=True)

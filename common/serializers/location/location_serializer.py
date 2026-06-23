from rest_framework import serializers

class LocationSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False, allow_null=True)
    locationName = serializers.CharField(required=True)
    city = serializers.CharField(required=True)
    state = serializers.CharField(required=True)
    country = serializers.CharField(required=True)
    address1 = serializers.CharField(required=True)
    address2 = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    employeeCount = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    zipCode = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    companyId = serializers.IntegerField(required=True)
    externalId = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    geofenceId = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    isActive = serializers.IntegerField(required=False, allow_null=True)
    payPeriod = serializers.IntegerField(required=False, allow_null=True)
    payPeriodStart = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    payPeriodEnd = serializers.CharField(required=False, allow_null=True, allow_blank=True)

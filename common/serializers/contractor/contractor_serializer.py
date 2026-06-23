from rest_framework import serializers

class ContractorSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False, allow_null=True)
    contractorName = serializers.CharField(required=False, allow_null=True)

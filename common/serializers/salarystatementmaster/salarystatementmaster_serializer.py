from rest_framework import serializers

class SalaryStatementMasterSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False, allow_null=True)
    companyId = serializers.IntegerField(required=False, allow_null=True)
    month = serializers.IntegerField(required=False, allow_null=True)
    year = serializers.IntegerField(required=False, allow_null=True)
    totalSalary = serializers.IntegerField(required=False, allow_null=True)
    totalPf = serializers.IntegerField(required=False, allow_null=True)
    totalPt = serializers.IntegerField(required=False, allow_null=True)
    note = serializers.CharField(required=False, allow_null=True)

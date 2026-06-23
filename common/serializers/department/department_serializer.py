from rest_framework import serializers

class DepartmentSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False, allow_null=True)
    departmentName = serializers.CharField(required=False, allow_null=True)
    companyId = serializers.IntegerField(required=False, allow_null=True)

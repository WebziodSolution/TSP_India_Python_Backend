from rest_framework import serializers

class EmployeeBackAccountInfoSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False, allow_null=True)
    accountType = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    ifscCode = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    bankName = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    branch = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    accountNumber = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    address = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    employeeId = serializers.IntegerField(required=False, allow_null=True)
    passbookImage = serializers.CharField(required=False, allow_null=True, allow_blank=True)

    def to_internal_value(self, data):
        if hasattr(data, 'dict'):
            data = data.dict()
        else:
            data = dict(data)
        
        for field_name, field in self.fields.items():
            if not isinstance(field, serializers.CharField):
                if field_name in data and data[field_name] == "":
                    data[field_name] = None
                    
        return super().to_internal_value(data)

from rest_framework import serializers

class EmployeeSerializer(serializers.Serializer):
    employeeId = serializers.IntegerField(required=False, allow_null=True)
    companyId = serializers.IntegerField(required=True)
    roleId = serializers.IntegerField(required=True)
    userName = serializers.CharField(required=True)
    firstName = serializers.CharField(required=True)
    lastName = serializers.CharField(required=True)
    email = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    password = serializers.CharField(required=True)
    phone = serializers.CharField(required=True)
    profileImage = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    companyEmployeeRolesDto = serializers.JSONField(required=False, allow_null=True)  # Nested: CompanyEmployeeRolesSerializer
    gender = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    dob = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    zipCode = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    city = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    state = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    country = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    hourlyRate = serializers.FloatField(required=False, allow_null=True)
    address1 = serializers.CharField(required=True)
    address2 = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    roleName = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    companyLocation = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    roles = serializers.JSONField(required=False, allow_null=True)  # Nested: List<CompanyEmployeeRolesDto>

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

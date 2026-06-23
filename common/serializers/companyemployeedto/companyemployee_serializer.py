from rest_framework import serializers

class CompanyEmployeeSerializer(serializers.Serializer):
    employeeId = serializers.IntegerField(required=False, allow_null=True)
    companyId = serializers.IntegerField(required=True)
    roleId = serializers.IntegerField(required=True)
    userName = serializers.CharField(required=True)
    firstName = serializers.CharField(required=True)
    lastName = serializers.CharField(required=True)
    email = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    password = serializers.CharField(required=True)
    phone = serializers.CharField(required=True)
    emergencyPhone = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    altPhone = serializers.CharField(required=False, allow_null=True, allow_blank=True)
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
    middleName = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    emergencyContact = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    contactPhone = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    relationship = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    departmentId = serializers.IntegerField(required=False, allow_null=True)
    departmentName = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    employeeTypeId = serializers.IntegerField(required=False, allow_null=True)
    employeeTypeName = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    payPeriod = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    payClass = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    hiredDate = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    bankAccountId = serializers.IntegerField(required=False, allow_null=True)
    isActive = serializers.IntegerField(required=False, allow_null=True)
    themeId = serializers.IntegerField(required=False, allow_null=True)
    shiftId = serializers.IntegerField(required=False, allow_null=True)
    companyLocation = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    checkGeofence = serializers.IntegerField(required=False, allow_null=True)
    embedding = serializers.ListField(child=serializers.FloatField(), required=False, allow_null=True)
    bloodGroup = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    aadharImage = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    isPf = serializers.BooleanField(default=False)
    pfType = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    pfPercentage = serializers.IntegerField(required=False, allow_null=True)
    pfAmount = serializers.IntegerField(required=False, allow_null=True)
    isPt = serializers.BooleanField(default=False)
    ptAmount = serializers.IntegerField(required=False, allow_null=True)
    basicSalary = serializers.IntegerField(required=False, allow_null=True)
    grossSalary = serializers.IntegerField(required=False, allow_null=True)
    canteenType = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    canteenAmount = serializers.IntegerField(required=False, allow_null=True)
    otId = serializers.IntegerField(required=False, allow_null=True)
    lunchBreak = serializers.IntegerField(required=False, allow_null=True)
    workingHoursIncludeLunch = serializers.FloatField(required=False, allow_null=True)
    weeklyOffId = serializers.IntegerField(required=False, allow_null=True)
    holidayTemplateId = serializers.IntegerField(required=False, allow_null=True)
    earlyExitPenaltyRule = serializers.BooleanField(default=False)
    lateEntryPenaltyRule = serializers.BooleanField(default=False)
    companyShiftDto = serializers.JSONField(required=False, allow_null=True)  # Nested: CompanyShiftSerializer
    employeeBackAccountInfoDTO = serializers.JSONField(required=False, allow_null=True)  # Nested: EmployeeBackAccountInfoSerializer

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

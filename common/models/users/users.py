from django.db import models

class Users(models.Model):
    userId = models.BigAutoField(primary_key=True, db_column='user_Id')
    firstName = models.CharField(max_length=255, null=True, blank=True, db_column='first_name')
    lastName = models.CharField(max_length=255, null=True, blank=True, db_column='last_name')
    middleName = models.CharField(max_length=255, null=True, blank=True, db_column='middle_name')
    email = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=255)
    password = models.CharField(max_length=255, null=True, blank=True)
    personalIdentificationNumber = models.CharField(max_length=255, null=True, blank=True, db_column='personal_identification_number')
    gender = models.CharField(max_length=255, null=True, blank=True)
    hourlyRate = models.BigIntegerField(null=True, blank=True, db_column='hourly_rate')
    address1 = models.CharField(max_length=255, null=True, blank=True)
    address2 = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    zipCode = models.CharField(max_length=255, null=True, blank=True, db_column='zip_code')
    country = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    birthDate = models.CharField(max_length=255, null=True, blank=True, db_column='birth_date')
    emergencyContact = models.CharField(max_length=255, null=True, blank=True, db_column='emergency_contact')
    contactPhone = models.CharField(max_length=255, null=True, blank=True, db_column='contact_phone')
    relationship = models.CharField(max_length=255, null=True, blank=True)
    department = models.ForeignKey('Department', on_delete=models.SET_NULL, db_column='department_id', null=True, blank=True, related_name='+')
    role = models.ForeignKey('Roles', on_delete=models.SET_NULL, db_column='role_id', null=True, blank=True, related_name='+')
    userShift = models.ForeignKey('UserShift', on_delete=models.SET_NULL, db_column='user_shift_id', null=True, blank=True, related_name='+')
    contractor = models.ForeignKey('Contractor', on_delete=models.SET_NULL, db_column='contractor_id', null=True, blank=True, related_name='+')
    profileImage = models.CharField(max_length=255, null=True, blank=True, db_column='profile_img')
    employeeId = models.CharField(max_length=255, null=True, blank=True, db_column='employee_id')
    userName = models.CharField(max_length=255, null=True, blank=True, db_column='user_name')

    class Meta:
        db_table = 'users'
        app_label = 'common'

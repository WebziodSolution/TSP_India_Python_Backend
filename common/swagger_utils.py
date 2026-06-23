from rest_framework import serializers
from drf_spectacular.extensions import OpenApiAuthenticationExtension

class JWTAuthenticationScheme(OpenApiAuthenticationExtension):
    target_class = 'common.auth.authentication.JWTAuthentication'
    name = 'BearerAuth'

    def get_security_definition(self, auto_schema):
        return {
            'type': 'http',
            'scheme': 'bearer',
            'bearerFormat': 'JWT',
            'description': 'Enter JWT token in format: "Bearer <token>"'
        }

_serializer_cache = {}

def get_api_response_serializer(result_serializer=None, many=False, name="ApiResponse"):
    """
    Dynamically generates an ApiResponse serializer wrapping the given result serializer/field.
    """
    cache_key = (result_serializer, many, name)
    if cache_key in _serializer_cache:
        return _serializer_cache[cache_key]

    if result_serializer:
        if isinstance(result_serializer, type) and issubclass(result_serializer, serializers.BaseSerializer):
            result_field = result_serializer(many=many, required=False)
        else:
            result_field = result_serializer
    else:
        result_field = serializers.JSONField(required=False, default=dict)

    class DynamicApiResponseSerializer(serializers.Serializer):
        status = serializers.IntegerField(help_text="HTTP status code")
        message = serializers.CharField(help_text="Response message detail")
        result = result_field

        class Meta:
            ref_name = f"{name}Wrapper"

    _serializer_cache[cache_key] = DynamicApiResponseSerializer
    return DynamicApiResponseSerializer


class LoginResponseDataSerializer(serializers.Serializer):
    userId = serializers.IntegerField(required=False)
    employeeId = serializers.IntegerField(required=False)
    userName = serializers.CharField()
    firstName = serializers.CharField()
    lastName = serializers.CharField()
    middleName = serializers.CharField(required=False, allow_null=True)
    email = serializers.CharField()
    phone = serializers.CharField()
    gender = serializers.CharField(required=False, allow_null=True)
    hourlyRate = serializers.IntegerField(required=False, allow_null=True)
    personalIdentificationNumber = serializers.CharField(required=False)
    address1 = serializers.CharField(required=False, allow_null=True)
    address2 = serializers.CharField(required=False, allow_null=True)
    city = serializers.CharField(required=False, allow_null=True)
    zipCode = serializers.CharField(required=False, allow_null=True)
    country = serializers.CharField(required=False, allow_null=True)
    state = serializers.CharField(required=False, allow_null=True)
    birthDate = serializers.CharField(required=False, allow_null=True)
    dob = serializers.CharField(required=False, allow_null=True)
    emergencyContact = serializers.CharField(required=False, allow_null=True)
    contactPhone = serializers.CharField(required=False, allow_null=True)
    relationship = serializers.CharField(required=False, allow_null=True)
    roleId = serializers.IntegerField(required=False, allow_null=True)
    roleName = serializers.CharField(required=False, allow_null=True)
    profileImage = serializers.CharField(required=False, allow_null=True)
    departmentId = serializers.IntegerField(required=False, allow_null=True)
    departmentName = serializers.CharField(required=False, allow_null=True)
    themeId = serializers.IntegerField(required=False, allow_null=True)
    companyId = serializers.IntegerField(required=False, allow_null=True)

class LoginResponseSerializer(serializers.Serializer):
    token = serializers.CharField()
    data = LoginResponseDataSerializer()
    error = serializers.CharField(required=False)
    errorType = serializers.CharField(required=False)

class UploadProfileImageSerializer(serializers.Serializer):
    userId = serializers.IntegerField(required=False, allow_null=True, help_text="User ID (optional, defaults to token user)")
    profileImage = serializers.CharField(required=True, help_text="Base64 encoded profile image string")

class StartUploadSerializer(serializers.Serializer):
    folderName = serializers.CharField(required=True)
    userId = serializers.IntegerField(required=False, allow_null=True)
    fileName = serializers.CharField(required=True)

class UploadChunkSerializer(serializers.Serializer):
    folderName = serializers.CharField(required=True)
    userId = serializers.IntegerField(required=False, allow_null=True)
    uploadId = serializers.CharField(required=True)
    chunkIndex = serializers.IntegerField(required=True)
    totalChunks = serializers.IntegerField(required=True)
    originalFileName = serializers.CharField(required=True)
    chunk = serializers.FileField(required=True, help_text="The chunk file upload")

class CompleteUploadSerializer(serializers.Serializer):
    folderName = serializers.CharField(required=True)
    userId = serializers.IntegerField(required=False, allow_null=True)
    uploadId = serializers.CharField(required=True)
    totalChunks = serializers.IntegerField(required=True)
    originalFileName = serializers.CharField(required=True)



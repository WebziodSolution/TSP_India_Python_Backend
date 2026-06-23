import logging
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter
from common.response.api_response import ApiResponse
from common.auth.authentication import JWTAuthentication
from common.exception.exceptions import GlobalException
from common.serializers import UserSerializer, LoginSerializer, ResetPasswordSerializer
from common.swagger_utils import (
    get_api_response_serializer,
    LoginResponseSerializer,
    UploadProfileImageSerializer
)
from .service import UserService

logger = logging.getLogger(__name__)
user_service = UserService()

@extend_schema(
    summary="Get all users",
    description="Retrieve a list of all users in the system, with optional filtering for company employees.",
    parameters=[
        OpenApiParameter(name="companyId", description="Filter by company ID", required=False, type=int),
        OpenApiParameter(name="departmentIds", description="Filter by department IDs (comma-separated)", required=False, type=str),
        OpenApiParameter(name="employeeIds", description="Filter by employee IDs (comma-separated)", required=False, type=str),
    ],
    responses={200: get_api_response_serializer(UserSerializer, many=True, name="UserList")}
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def get_all_users(request):
    try:
        company_id = request.query_params.get('companyId')
        dept_ids_str = request.query_params.get('departmentIds')
        emp_ids_str = request.query_params.get('employeeIds')

        company_id = int(company_id) if company_id else None

        dept_ids = None
        if dept_ids_str:
            dept_ids = [int(x.strip()) for x in dept_ids_str.split(',') if x.strip()]

        emp_ids = None
        if emp_ids_str:
            emp_ids = [int(x.strip()) for x in emp_ids_str.split(',') if x.strip()]

        users = user_service.get_all_users(
            company_id=company_id,
            department_ids=dept_ids,
            employee_ids=emp_ids
        )
        return ApiResponse(status.HTTP_200_OK, "User fetched successfully", users)
    except Exception as e:
        logger.error(f"getAllUsers view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e), {})

@extend_schema(
    summary="Get user by ID",
    description="Retrieve a specific user details by ID.",
    parameters=[
        OpenApiParameter(name="id", description="User ID", required=True, type=str, location=OpenApiParameter.PATH)
    ],
    responses={
        200: get_api_response_serializer(UserSerializer, name="UserDetail"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def get_user(request, id):
    try:
        user_id = int(id)
        user = user_service.get_user_by_id(user_id)
        return ApiResponse(status.HTTP_200_OK, "User fetched successfully", user)
    except Exception as e:
        logger.error(f"getUser view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e), {})

@extend_schema(
    summary="Create a new user",
    description="Create a new user in the system.",
    request=UserSerializer,
    responses={
        201: get_api_response_serializer(UserSerializer, name="UserCreated"),
        400: get_api_response_serializer(name="ValidationError"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['POST'])
@permission_classes([AllowAny])
def create_user(request):
    try:
        # Validate data in serializer or dict (Java does standard validation)
        # We can extract data from request
        data = request.data
        res = user_service.create_user(data)
        return ApiResponse(status.HTTP_201_CREATED, "User added successfully", res)
    except GlobalException as e:
        logger.error(f"createUser validation error: {e}")
        return ApiResponse(status.HTTP_400_BAD_REQUEST, str(e), {})
    except Exception as e:
        logger.error(f"createUser internal error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e), {})

@extend_schema(
    summary="Update user details",
    description="Update an existing user's details.",
    parameters=[
        OpenApiParameter(name="id", description="User ID", required=True, type=str, location=OpenApiParameter.PATH)
    ],
    request=UserSerializer,
    responses={
        200: get_api_response_serializer(name="UserUpdated"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
def update_user(request, id):
    try:
        user_id = int(id)
        data = request.data
        user_service.update_user(user_id, data)
        return ApiResponse(status.HTTP_200_OK, "User updated successfully", "")
    except Exception as e:
        logger.error(f"updateUser view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e), {})

@extend_schema(
    summary="Delete a user",
    description="Remove a user from the system by ID.",
    parameters=[
        OpenApiParameter(name="id", description="User ID", required=True, type=str, location=OpenApiParameter.PATH)
    ],
    responses={
        200: get_api_response_serializer(name="UserDeleted"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
def delete_user(request, id):
    try:
        user_id = int(id)
        user_service.delete_user(user_id)
        return ApiResponse(status.HTTP_200_OK, "User deleted successfully", "")
    except Exception as e:
        logger.error(f"deleteUser view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e), {})

@extend_schema(
    summary="User Login",
    description="Authenticate user with username, password and company ID.",
    request=LoginSerializer,
    responses={
        200: get_api_response_serializer(LoginResponseSerializer, name="LoginSuccess"),
        400: get_api_response_serializer(name="LoginFailed"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['POST'])
@permission_classes([AllowAny])
def user_login(request):
    try:
        res_body = user_service.user_login(request.data)
        if "error" in res_body:
            return ApiResponse(status.HTTP_400_BAD_REQUEST, res_body["error"], res_body)
        if not res_body:
            return ApiResponse(status.HTTP_400_BAD_REQUEST, "Invalid credentials", res_body)
        return ApiResponse(status.HTTP_200_OK, "Login successful", res_body)
    except Exception as e:
        logger.error(f"userLogin view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "failed to login", {})

@extend_schema(
    summary="Generate Password Reset Link",
    description="Generate a password reset link and send it via email.",
    parameters=[
        OpenApiParameter(name="email", description="Registered email address", required=True, type=str),
        OpenApiParameter(name="userName", description="User's username", required=True, type=str),
        OpenApiParameter(name="companyId", description="Company ID", required=True, type=str)
    ],
    responses={
        200: get_api_response_serializer(name="ResetLinkGenerated"),
        400: get_api_response_serializer(name="InvalidRequest"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['GET'])
@permission_classes([AllowAny])
def generate_reset_link(request):
    try:
        email = request.query_params.get('email')
        user_name = request.query_params.get('userName')
        company_id = request.query_params.get('companyId')
        
        if not all([email, user_name, company_id]):
            return ApiResponse(status.HTTP_400_BAD_REQUEST, "Missing required parameters: email, userName, companyId", {})
            
        if user_service.generate_reset_link(email, user_name, company_id):
            return ApiResponse(status.HTTP_200_OK, f"A password reset link has been sent to {email}", "")
        else:
            return ApiResponse(status.HTTP_400_BAD_REQUEST, "This email or username is not registered", "")
    except Exception as e:
        logger.error(f"generateResetLink view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Fail to generate link", {})

@extend_schema(
    summary="Validate Reset Token",
    description="Validate a password reset token.",
    parameters=[
        OpenApiParameter(name="token", description="Token to validate", required=True, type=str)
    ],
    responses={
        200: get_api_response_serializer(name="TokenValid"),
        400: get_api_response_serializer(name="TokenInvalid"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['GET'])
@permission_classes([AllowAny])
def validate_token(request):
    try:
        token = request.query_params.get('token')
        if not token:
            return ApiResponse(status.HTTP_400_BAD_REQUEST, "Missing token parameter", {})
            
        validate_res = user_service.validate_token(token)
        if validate_res is not None:
            return ApiResponse(status.HTTP_200_OK, validate_res.get("message", "Token is valid"), validate_res)
        return ApiResponse(status.HTTP_400_BAD_REQUEST, "Invalid token", "")
    except Exception as e:
        logger.error(f"validateToken view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Fail to fetch account details", {})

@extend_schema(
    summary="Reset Password",
    description="Reset user password / PIN using a reset token or current password.",
    request=ResetPasswordSerializer,
    responses={
        200: get_api_response_serializer(name="PasswordResetSuccess"),
        400: get_api_response_serializer(name="PasswordResetFailed"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['POST'])
@permission_classes([AllowAny])
def reset_password(request):
    try:
        response = user_service.reset_password(request.data)
        if "success" in response:
            return ApiResponse(status.HTTP_200_OK, "Pin reset successfully", response)
        return ApiResponse(status.HTTP_400_BAD_REQUEST, "Failed to reset pin", response)
    except Exception as e:
        logger.error(f"resetPassword view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Error resetting pin", {"error": str(e)})

@extend_schema(
    summary="Upload Profile Image",
    description="Upload a new profile image. If userId is not specified, it is extracted from the JWT.",
    request=UploadProfileImageSerializer,
    responses={
        200: get_api_response_serializer(name="ProfileImageUploaded"),
        400: get_api_response_serializer(name="InvalidImage"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
def upload_profile_image(request):
    try:
        req = request.data
        auth_header = request.headers.get('Authorization') or request.META.get('HTTP_AUTHORIZATION')
        
        user_id_val = req.get("userId")
        if user_id_val is not None:
            user_id = int(user_id_val)
        else:
            # extract from token
            token = auth_header[7:]
            user_id = int(user_service.jwt_util.extract_user_id(token))
            
        profile_img = req.get("profileImage")
        if not profile_img:
            return ApiResponse(status.HTTP_400_BAD_REQUEST, "profileImage parameter is required", "")
            
        path = user_service.upload_profile_image(user_id, profile_img)
        if path == "Error":
            return ApiResponse(status.HTTP_404_NOT_FOUND, "Image does not exist in the directory", "")
        return ApiResponse(status.HTTP_200_OK, "Profile image update successfully", path)
    except Exception as e:
        logger.error(f"uploadProfileImage view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Fail to update profile image", {})

@extend_schema(
    summary="Delete Profile Image",
    description="Delete the profile image for the authenticated user.",
    responses={
        200: get_api_response_serializer(name="ProfileImageDeleted"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def delete_profile_image(request):
    try:
        auth_header = request.headers.get('Authorization') or request.META.get('HTTP_AUTHORIZATION')
        token = auth_header[7:]
        user_id = int(user_service.jwt_util.extract_user_id(token))
        
        if user_service.delete_profile_image(user_id):
            return ApiResponse(status.HTTP_200_OK, "Profile image deleted successfully", "")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Profile image not found", "")
    except Exception as e:
        logger.error(f"deleteProfileImage view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Fail to delete profile image", {})


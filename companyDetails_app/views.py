import logging
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework import serializers
from drf_spectacular.utils import extend_schema, OpenApiParameter
from common.response.api_response import ApiResponse
from common.auth.authentication import JWTAuthentication
from common.exception.exceptions import GlobalException
from common.serializers import CompanyDetailsSerializer
from common.swagger_utils import get_api_response_serializer
from .service import CompanyDetailsService

logger = logging.getLogger(__name__)
company_details_service = CompanyDetailsService()

# Helper Serializers for Request Bodies
class UploadCompanyLogoRequestSerializer(serializers.Serializer):
    companyId = serializers.IntegerField(required=True, help_text="Company ID")
    companyLogo = serializers.CharField(required=True, help_text="Company Logo path or base64 data")

class UpdateAutoTimeRequestSerializer(serializers.Serializer):
    time = serializers.CharField(required=True, help_text="Auto time string (e.g., '20:00')")


@extend_schema(
    summary="Search Companies",
    description="Search companies by name and active status.",
    parameters=[
        OpenApiParameter(name="name", description="Company Name search term", required=True, type=str),
        OpenApiParameter(name="active", description="Active filter (0=inactive, 1=active, other=all)", required=True, type=int)
    ],
    responses={
        200: get_api_response_serializer(name="SearchCompaniesList"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def search(request):
    try:
        name = request.query_params.get("name", "")
        active_str = request.query_params.get("active", "")
        active = int(active_str) if active_str else 2
        
        result = company_details_service.search_companies(name, active)
        return ApiResponse(status.HTTP_200_OK, "Fetch company details successfully", result)
    except Exception as e:
        logger.error(f"search view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Fail to fetch company details", {})


@extend_schema(
    summary="Get All Company Details",
    description="Retrieve a simplified list of all companies.",
    parameters=[
        OpenApiParameter(name="active", description="Active filter (0=inactive, 1=active, 2=all)", required=True, type=int)
    ],
    responses={
        200: get_api_response_serializer(name="AllCompanyDetailsList"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def get_all_company_details(request):
    try:
        active_str = request.query_params.get("active", "")
        active = int(active_str) if active_str else 2
        
        result = company_details_service.get_all_company_details(active)
        return ApiResponse(status.HTTP_200_OK, "Fetch company details successfully", result)
    except Exception as e:
        logger.error(f"get_all_company_details view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Fail to fetch company details", {})


@extend_schema(
    summary="Get Company Details by ID",
    description="Retrieve full company details, including nested locations.",
    parameters=[
        OpenApiParameter(name="id", description="Company ID", required=True, type=int, location=OpenApiParameter.PATH)
    ],
    responses={
        200: get_api_response_serializer(CompanyDetailsSerializer, name="CompanyDetailsResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def get_company_details(request, id):
    try:
        company_id = int(id)
        result = company_details_service.get_company_details(company_id)
        return ApiResponse(status.HTTP_200_OK, "Fetch company details successfully", result)
    except Exception as e:
        logger.error(f"get_company_details view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Fail to fetch company details", {})


@extend_schema(
    summary="Create Company Details",
    description="Add new company details for step 1.",
    parameters=[
        OpenApiParameter(name="step", description="Creation step ('1')", required=True, type=str, location=OpenApiParameter.PATH)
    ],
    request=CompanyDetailsSerializer,
    responses={
        201: get_api_response_serializer(CompanyDetailsSerializer, name="CompanyCreatedResponse"),
        400: get_api_response_serializer(name="ValidationError"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['POST'])
@permission_classes([AllowAny])
def create_company_details(request, step):
    try:
        result = company_details_service.create_company_details(request.data, step)
        return ApiResponse(status.HTTP_201_CREATED, "Company details added successfully", result)
    except GlobalException as e:
        logger.error(f"create_company_details validation error: {e}")
        return ApiResponse(status.HTTP_400_BAD_REQUEST, str(e), {})
    except Exception as e:
        logger.error(f"create_company_details view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e), {})


@extend_schema(
    summary="Update Company Details",
    description="Update company details for step 1 or step 3.",
    parameters=[
        OpenApiParameter(name="id", description="Company ID", required=True, type=int, location=OpenApiParameter.PATH),
        OpenApiParameter(name="step", description="Update step ('1' or '3')", required=True, type=str, location=OpenApiParameter.PATH)
    ],
    request=CompanyDetailsSerializer,
    responses={
        200: get_api_response_serializer(CompanyDetailsSerializer, name="CompanyUpdatedResponse"),
        400: get_api_response_serializer(name="ValidationError"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
def update_company_details(request, id, step):
    try:
        company_id = int(id)
        result = company_details_service.update_company_details(company_id, request.data, step)
        # if result is None:
        #     return ApiResponse(status.HTTP_400_BAD_REQUEST, "Invalid step or operation failed", {})
        return ApiResponse(status.HTTP_200_OK, "Company details updated successfully", result)
    except GlobalException as e:
        logger.error(f"update_company_details validation error: {e}")
        return ApiResponse(status.HTTP_400_BAD_REQUEST, str(e), {})
    except Exception as e:
        logger.error(f"update_company_details view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e), {})


@extend_schema(
    summary="Delete Company Details",
    description="Remove company details by ID.",
    parameters=[
        OpenApiParameter(name="id", description="Company ID", required=True, type=int, location=OpenApiParameter.PATH)
    ],
    responses={
        200: get_api_response_serializer(name="CompanyDeletedResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
def delete_company_details(request, id):
    try:
        company_id = int(id)
        company_details_service.delete_company_details(company_id)
        return ApiResponse(status.HTTP_200_OK, "Company deactivate successfully", "")
    except Exception as e:
        logger.error(f"delete_company_details view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Fail to fetch delet company details", {})


@extend_schema(
    summary="Upload Company Logo",
    description="Upload a new logo image for a company.",
    request=UploadCompanyLogoRequestSerializer,
    responses={
        200: get_api_response_serializer(name="LogoUploadResponse"),
        404: get_api_response_serializer(name="LogoNotFoundError"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
def upload_company_logo(request):
    try:
        company_id_val = request.data.get("companyId")
        logo_path = request.data.get("companyLogo")
        
        if not company_id_val or not logo_path:
            return ApiResponse(status.HTTP_400_BAD_REQUEST, "Missing companyId or companyLogo", {})
            
        company_id = int(company_id_val)
        path = company_details_service.upload_company_logo(company_id, logo_path)
        if path == "Error":
            return ApiResponse(status.HTTP_404_NOT_FOUND, "Image does not exist in the directory", "")
        return ApiResponse(status.HTTP_200_OK, "Logo update successfully", path)
    except Exception as e:
        logger.error(f"upload_company_logo view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Fail to update profile image", {})


@extend_schema(
    summary="Delete Company Logo",
    description="Delete the logo image for a company.",
    parameters=[
        OpenApiParameter(name="companyId", description="Company ID", required=True, type=int, location=OpenApiParameter.PATH)
    ],
    responses={
        200: get_api_response_serializer(name="LogoDeleteResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
def delete_company_logo(request, companyId):
    try:
        company_id = int(companyId)
        if company_details_service.delete_company_logo(company_id):
            return ApiResponse(status.HTTP_200_OK, "Logo deleted successfully", "")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Logo not found", "")
    except Exception as e:
        logger.error(f"delete_company_logo view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Fail to delete profile image", {})


@extend_schema(
    summary="Get Last Company",
    description="Fetch the company number of the last registered company.",
    responses={
        200: get_api_response_serializer(name="LastCompanyResponse"),
        404: get_api_response_serializer(name="LastCompanyNotFoundError"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def get_last_company(request):
    try:
        company_no = company_details_service.get_last_company()
        if company_no:
            return ApiResponse(status.HTTP_200_OK, "Fetch company details successfully", company_no)
        return ApiResponse(status.HTTP_404_NOT_FOUND, "No company details found", "")
    except Exception as e:
        logger.error(f"get_last_company view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Fail to fetch company details", {})


@extend_schema(
    summary="Update Auto Time In After Hours",
    description="Update the auto time in after hours setting for a company.",
    parameters=[
        OpenApiParameter(name="companyId", description="Company ID", required=True, type=int, location=OpenApiParameter.PATH)
    ],
    request=UpdateAutoTimeRequestSerializer,
    responses={
        200: get_api_response_serializer(name="UpdateAutoTimeResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
def update_auto_time_in_after_hours(request, companyId):
    try:
        company_id = int(companyId)
        time_str = request.data.get("time")
        if not time_str:
            return ApiResponse(status.HTTP_400_BAD_REQUEST, "Missing time parameter", {})
            
        company_details_service.update_auto_time_in_after_hours(company_id, time_str)
        return ApiResponse(status.HTTP_200_OK, "Company details updated successfully", "")
    except Exception as e:
        logger.error(f"update_auto_time_in_after_hours view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Fail to update company details", {})


@extend_schema(
    summary="Get Auto Time In After Hours",
    description="Fetch the auto time in after hours setting for a company.",
    parameters=[
        OpenApiParameter(name="companyId", description="Company ID", required=True, type=int, location=OpenApiParameter.PATH)
    ],
    responses={
        200: get_api_response_serializer(name="GetAutoTimeResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def get_auto_time_in_after_hours(request, companyId):
    try:
        company_id = int(companyId)
        time_val = company_details_service.get_auto_time_in_after_hours(company_id)
        return ApiResponse(status.HTTP_200_OK, "Company details fetched successfully", time_val)
    except Exception as e:
        logger.error(f"get_auto_time_in_after_hours view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Fail to fetch company details", {})

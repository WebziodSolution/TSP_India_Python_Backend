import logging
from rest_framework.decorators import api_view, authentication_classes
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter
from common.response.api_response import ApiResponse
from common.auth.authentication import JWTAuthentication
from common.serializers import CompanyThemeSerializer
from common.swagger_utils import get_api_response_serializer
from .service import CompanyThemeService

logger = logging.getLogger(__name__)
theme_service = CompanyThemeService()

@extend_schema(
    summary="Get All Company Themes by Company ID",
    description="Retrieve the company theme settings for a given company ID.",
    parameters=[
        OpenApiParameter(name="id", description="Company ID", required=True, type=int, location=OpenApiParameter.PATH)
    ],
    responses={
        200: get_api_response_serializer(CompanyThemeSerializer, name="CompanyThemeResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def get_all_company_theme(request, id):
    try:
        company_id = int(id)
        result = theme_service.get_all_theme(company_id)
        return ApiResponse(status.HTTP_200_OK, "Fetch theme details successfully", result)
    except Exception as e:
        logger.error(f"get_all_company_theme view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Fail to fetch theme details", {})


@extend_schema(
    summary="Get Company Theme by ID",
    description="Retrieve details of a company theme by theme ID.",
    parameters=[
        OpenApiParameter(name="id", description="Theme ID", required=True, type=int, location=OpenApiParameter.PATH)
    ],
    responses={
        200: get_api_response_serializer(CompanyThemeSerializer, name="CompanyThemeResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def get_company_theme(request, id):
    try:
        theme_id = int(id)
        result = theme_service.get_theme(theme_id)
        return ApiResponse(status.HTTP_200_OK, "Fetch theme details successfully", result)
    except Exception as e:
        logger.error(f"get_company_theme view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Fail to fetch theme details", {})


@extend_schema(
    summary="Create Company Theme",
    description="Create theme settings for a company.",
    request=CompanyThemeSerializer,
    responses={
        201: get_api_response_serializer(name="ThemeCreatedResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
def create_company_theme(request):
    try:
        theme_service.create_theme(request.data)
        return ApiResponse(status.HTTP_201_CREATED, "Theme created successfully", "")
    except Exception as e:
        logger.error(f"create_company_theme view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e), {})


@extend_schema(
    summary="Update Company Theme",
    description="Update some or all parameters of a company's theme by ID.",
    parameters=[
        OpenApiParameter(name="id", description="Theme ID", required=True, type=int, location=OpenApiParameter.PATH)
    ],
    request=CompanyThemeSerializer,
    responses={
        200: get_api_response_serializer(name="ThemeUpdatedResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
def update_company_theme(request, id):
    try:
        theme_id = int(id)
        result = theme_service.update_theme(theme_id, request.data)
        if result is None:
            return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Theme not found", {})
        return ApiResponse(status.HTTP_200_OK, "Theme updated successfully", "")
    except Exception as e:
        logger.error(f"update_company_theme view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e), {})


@extend_schema(
    summary="Delete Company Theme",
    description="Delete theme settings for a company.",
    parameters=[
        OpenApiParameter(name="id", description="Theme ID", required=True, type=int, location=OpenApiParameter.PATH)
    ],
    responses={
        200: get_api_response_serializer(name="ThemeDeletedResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
def delete_company_theme(request, id):
    try:
        theme_id = int(id)
        theme_service.delete_theme(theme_id)
        return ApiResponse(status.HTTP_200_OK, "Theme deleted successfully", "")
    except Exception as e:
        logger.error(f"delete_company_theme view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e), {})

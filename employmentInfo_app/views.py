import logging
from rest_framework.decorators import api_view, authentication_classes
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter
from common.response.api_response import ApiResponse
from common.auth.authentication import JWTAuthentication
from common.serializers import EmploymentInfoSerializer
from common.swagger_utils import get_api_response_serializer
from .service import EmploymentInfoService

logger = logging.getLogger(__name__)
employment_info_service = EmploymentInfoService()

@extend_schema(
    summary="Get All Employment Info",
    description="Retrieve a list of all employment info details.",
    responses={
        200: get_api_response_serializer(EmploymentInfoSerializer, many=True, name="EmploymentInfoListResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def get_all_employment_info(request):
    try:
        result = employment_info_service.get_all_employment_info()
        return ApiResponse(status.HTTP_200_OK, "Fetched employment info successfully", result)
    except Exception as e:
        logger.error(f"get_all_employment_info view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e), {})


@extend_schema(
    summary="Get Employment Info by ID",
    description="Retrieve details of an employment info by ID.",
    parameters=[
        OpenApiParameter(name="id", description="Employment Info ID", required=True, type=int, location=OpenApiParameter.PATH)
    ],
    responses={
        200: get_api_response_serializer(EmploymentInfoSerializer, name="EmploymentInfoResponse"),
        404: get_api_response_serializer(name="ErrorResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def get_employment_info_by_id(request, id):
    try:
        info_id = int(id)
        result = employment_info_service.get_employment_info_by_id(info_id)
        return ApiResponse(status.HTTP_200_OK, "Fetched employment info successfully", result)
    except Exception as e:
        logger.error(f"get_employment_info_by_id view error: {e}")
        if "not found" in str(e).lower():
            return ApiResponse(status.HTTP_404_NOT_FOUND, "Employment info not found", {})
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e), {})


@extend_schema(
    summary="Create Employment Info",
    description="Create a new employment info.",
    request=EmploymentInfoSerializer,
    responses={
        201: get_api_response_serializer(name="EmploymentInfoCreatedResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
def create_employment_info(request):
    try:
        employment_info_service.create_employment_info(request.data)
        return ApiResponse(status.HTTP_201_CREATED, "Employment info created successfully", "")
    except Exception as e:
        logger.error(f"create_employment_info view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e), {})


@extend_schema(
    summary="Update Employment Info",
    description="Update an existing employment info by ID.",
    parameters=[
        OpenApiParameter(name="id", description="Employment Info ID", required=True, type=int, location=OpenApiParameter.PATH)
    ],
    request=EmploymentInfoSerializer,
    responses={
        200: get_api_response_serializer(name="EmploymentInfoUpdatedResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
def update_employment_info(request, id):
    try:
        info_id = int(id)
        employment_info_service.update_employment_info(info_id, request.data)
        return ApiResponse(status.HTTP_200_OK, "Employment info updated successfully", "")
    except Exception as e:
        logger.error(f"update_employment_info view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e), {})


@extend_schema(
    summary="Delete Employment Info",
    description="Delete an existing employment info by ID.",
    parameters=[
        OpenApiParameter(name="id", description="Employment Info ID", required=True, type=int, location=OpenApiParameter.PATH)
    ],
    responses={
        200: get_api_response_serializer(name="EmploymentInfoDeletedResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
def delete_employment_info(request, id):
    try:
        info_id = int(id)
        employment_info_service.delete_employment_info(info_id)
        return ApiResponse(status.HTTP_200_OK, "Employment info deleted successfully", "")
    except Exception as e:
        logger.error(f"delete_employment_info view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e), {})

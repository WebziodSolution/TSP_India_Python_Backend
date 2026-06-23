import logging
from rest_framework.decorators import api_view, authentication_classes
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter
from common.response.api_response import ApiResponse
from common.auth.authentication import JWTAuthentication
from common.serializers import HolidayTemplateDetailsSerializer
from common.swagger_utils import get_api_response_serializer
from .service import HolidayTemplateDetailsService

logger = logging.getLogger(__name__)
details_service = HolidayTemplateDetailsService()

@extend_schema(
    summary="Get All Holiday Template Details",
    description="Retrieve all holiday template details associated with a template ID.",
    parameters=[
        OpenApiParameter(name="id", description="Template ID", required=True, type=int, location=OpenApiParameter.PATH)
    ],
    responses={
        200: get_api_response_serializer(HolidayTemplateDetailsSerializer, many=True, name="HolidayTemplateDetailsListResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def get_all_holiday_template_details_by_template_id(request, id):
    try:
        template_id = int(id)
        result = details_service.get_all_holiday_template_details_by_template_id(template_id)
        return ApiResponse(status.HTTP_200_OK, "Holiday template details fetched successfully", result)
    except Exception as e:
        logger.error(f"get_all_holiday_template_details_by_template_id view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e), {})


@extend_schema(
    summary="Get Holiday Template Details by ID",
    description="Retrieve holiday template details by record ID.",
    parameters=[
        OpenApiParameter(name="id", description="Record ID", required=True, type=int, location=OpenApiParameter.PATH)
    ],
    responses={
        200: get_api_response_serializer(HolidayTemplateDetailsSerializer, name="HolidayTemplateDetailsResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def get_holiday_template_details(request, id):
    try:
        record_id = int(id)
        result = details_service.get_holiday_template_details_by_id(record_id)
        return ApiResponse(status.HTTP_200_OK, "Holiday template details fetched successfully", result)
    except Exception as e:
        logger.error(f"get_holiday_template_details view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e), {})


@extend_schema(
    summary="Create Holiday Template Details",
    description="Create new holiday template details record.",
    request=HolidayTemplateDetailsSerializer,
    responses={
        201: get_api_response_serializer(name="HolidayTemplateDetailsCreatedResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
def create_holiday_template_details(request):
    try:
        details_service.create_holiday_template_details(request.data)
        return ApiResponse(status.HTTP_201_CREATED, "Holiday template details created successfully", "")
    except Exception as e:
        logger.error(f"create_holiday_template_details view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e), {})


@extend_schema(
    summary="Update Holiday Template Details",
    description="Update existing holiday template details by record ID.",
    parameters=[
        OpenApiParameter(name="id", description="Record ID", required=True, type=int, location=OpenApiParameter.PATH)
    ],
    request=HolidayTemplateDetailsSerializer,
    responses={
        200: get_api_response_serializer(name="HolidayTemplateDetailsUpdatedResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['PATCH'])
@authentication_classes([JWTAuthentication])
def update_holiday_template_details(request, id):
    try:
        record_id = int(id)
        details_service.update_holiday_template_details(record_id, request.data)
        return ApiResponse(status.HTTP_200_OK, "Holiday template details updated successfully", "")
    except Exception as e:
        logger.error(f"update_holiday_template_details view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e), {})


@extend_schema(
    summary="Delete Holiday Template Details",
    description="Delete holiday template details record by ID.",
    parameters=[
        OpenApiParameter(name="id", description="Record ID", required=True, type=int, location=OpenApiParameter.PATH)
    ],
    responses={
        200: get_api_response_serializer(name="HolidayTemplateDetailsDeletedResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
def delete_holiday_template_details(request, id):
    try:
        record_id = int(id)
        details_service.delete_holiday_template_details(record_id)
        return ApiResponse(status.HTTP_200_OK, "Holiday template details updated successfully", "")
    except Exception as e:
        logger.error(f"delete_holiday_template_details view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e), {})

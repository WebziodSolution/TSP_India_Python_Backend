import logging
from rest_framework.decorators import api_view, authentication_classes
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter
from common.response.api_response import ApiResponse
from common.auth.authentication import JWTAuthentication
from common.serializers import CompanyShiftSerializer
from common.swagger_utils import get_api_response_serializer
from .service import CompanyShiftService

logger = logging.getLogger(__name__)
shift_service = CompanyShiftService()

@extend_schema(
    summary="Get All Shifts for Company",
    description="Retrieve all shifts associated with a company ID.",
    parameters=[
        OpenApiParameter(name="companyId", description="Company ID", required=True, type=int, location=OpenApiParameter.PATH)
    ],
    responses={
        200: get_api_response_serializer(CompanyShiftSerializer, many=True, name="CompanyShiftsListResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def get_all_shifts(request, companyId):
    try:
        company_id = int(companyId)
        result = shift_service.get_all_shifts(company_id)
        return ApiResponse(status.HTTP_200_OK, "Shifts fetched successfully", result)
    except Exception as e:
        logger.error(f"get_all_shifts view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to fetch shifts", {})


@extend_schema(
    summary="Get Shift by ID",
    description="Retrieve details of a shift by shift ID.",
    parameters=[
        OpenApiParameter(name="id", description="Shift ID", required=True, type=int, location=OpenApiParameter.PATH)
    ],
    responses={
        200: get_api_response_serializer(CompanyShiftSerializer, name="CompanyShiftResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def get_shift_by_id(request, id):
    try:
        shift_id = int(id)
        result = shift_service.get_shift_by_id(shift_id)
        return ApiResponse(status.HTTP_200_OK, "Shifts fetched successfully", result)
    except Exception as e:
        logger.error(f"get_shift_by_id view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to fetch shifts", {})


@extend_schema(
    summary="Create Shift",
    description="Add a new company shift.",
    request=CompanyShiftSerializer,
    responses={
        201: get_api_response_serializer(name="ShiftCreatedResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
def create_shift(request):
    try:
        shift_service.create_shift(request.data)
        return ApiResponse(status.HTTP_201_CREATED, "Shifts created successfully", "")
    except Exception as e:
        logger.error(f"create_shift view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to create shift", {})


@extend_schema(
    summary="Update Shift",
    description="Update an existing company shift details by shift ID.",
    parameters=[
        OpenApiParameter(name="id", description="Shift ID", required=True, type=int, location=OpenApiParameter.PATH)
    ],
    request=CompanyShiftSerializer,
    responses={
        200: get_api_response_serializer(name="ShiftUpdatedResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
def update_shift(request, id):
    try:
        shift_id = int(id)
        shift_service.update_shift(shift_id, request.data)
        return ApiResponse(status.HTTP_200_OK, "Shifts updated successfully", "")
    except Exception as e:
        logger.error(f"update_shift view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to create shift", {})


@extend_schema(
    summary="Delete Shift",
    description="Delete an existing company shift by ID.",
    parameters=[
        OpenApiParameter(name="id", description="Shift ID", required=True, type=int, location=OpenApiParameter.PATH)
    ],
    responses={
        200: get_api_response_serializer(name="ShiftDeletedResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
def delete_shift(request, id):
    try:
        shift_id = int(id)
        shift_service.delete_shift(shift_id)
        return ApiResponse(status.HTTP_200_OK, "Shifts fetched successfully", "")
    except Exception as e:
        logger.error(f"delete_shift view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to fetch shifts", {})

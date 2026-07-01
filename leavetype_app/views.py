import logging
from rest_framework.decorators import api_view, authentication_classes
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter
from common.response.api_response import ApiResponse
from common.auth.authentication import JWTAuthentication
from common.serializers import LeaveTypeSerializer
from common.swagger_utils import get_api_response_serializer
from .service import LeaveTypeService

logger = logging.getLogger(__name__)
leave_type_service = LeaveTypeService()

@extend_schema(
    summary="Get All Leave Types",
    description="Retrieve details of all leave types associated with a company ID.",
    parameters=[
        OpenApiParameter(name="companyId", description="Company ID", required=True, type=int, location=OpenApiParameter.PATH)
    ],
    responses={
        200: get_api_response_serializer(LeaveTypeSerializer, many=True, name="LeaveTypesListResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def get_all_leave_types(request, companyId):
    try:
        comp_id = int(companyId)
        result = leave_type_service.get_all_leave_types(comp_id)
        return ApiResponse(status.HTTP_200_OK, "Fetch leave type details successfully", result)
    except Exception as e:
        logger.error(f"get_all_leave_types view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Fail to fetch leave type details", {})


@extend_schema(
    summary="Get Leave Type by ID",
    description="Retrieve details of a leave type by ID.",
    parameters=[
        OpenApiParameter(name="id", description="Leave Type ID", required=True, type=int, location=OpenApiParameter.PATH)
    ],
    responses={
        200: get_api_response_serializer(LeaveTypeSerializer, name="LeaveTypeResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def get_leave_type(request, id):
    try:
        lt_id = int(id)
        result = leave_type_service.get_leave_type(lt_id)
        return ApiResponse(status.HTTP_200_OK, "Fetch leave type details successfully", result)
    except Exception as e:
        logger.error(f"get_leave_type view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Fail to fetch leave type details", {})


@extend_schema(
    summary="Create Leave Type",
    description="Create a new leave type.",
    request=LeaveTypeSerializer,
    responses={
        201: get_api_response_serializer(name="LeaveTypeCreatedResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
def create_leave_type(request):
    try:
        leave_type_service.create_leave_type(request.data)
        return ApiResponse(status.HTTP_201_CREATED, "Create leave type details successfully", "")
    except Exception as e:
        logger.error(f"create_leave_type view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Fail to create leave type details", {})


@extend_schema(
    summary="Update Leave Type",
    description="Update an existing leave type by ID.",
    parameters=[
        OpenApiParameter(name="id", description="Leave Type ID", required=True, type=int, location=OpenApiParameter.PATH)
    ],
    request=LeaveTypeSerializer,
    responses={
        200: get_api_response_serializer(name="LeaveTypeUpdatedResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
def update_leave_type(request, id):
    try:
        lt_id = int(id)
        leave_type_service.update_leave_type(lt_id, request.data)
        return ApiResponse(status.HTTP_200_OK, "Update leave type details successfully", "")
    except Exception as e:
        logger.error(f"update_leave_type view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Fail to update leave type details", {})


@extend_schema(
    summary="Delete Leave Type",
    description="Delete an existing leave type by ID.",
    parameters=[
        OpenApiParameter(name="id", description="Leave Type ID", required=True, type=int, location=OpenApiParameter.PATH)
    ],
    responses={
        200: get_api_response_serializer(name="LeaveTypeDeletedResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
def delete_leave_type(request, id):
    try:
        lt_id = int(id)
        leave_type_service.delete_leave_type(lt_id)
        return ApiResponse(status.HTTP_200_OK, "Delete leave type details successfully", "")
    except Exception as e:
        logger.error(f"delete_leave_type view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Fail to delete leave type details", {})

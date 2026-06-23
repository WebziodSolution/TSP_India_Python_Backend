import logging
from rest_framework.decorators import api_view, authentication_classes
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter
from common.response.api_response import ApiResponse
from common.auth.authentication import JWTAuthentication
from common.serializers import EmployeeTypeSerializer
from common.swagger_utils import get_api_response_serializer
from .service import EmployeeTypeService

logger = logging.getLogger(__name__)
employee_type_service = EmployeeTypeService()

@extend_schema(
    summary="Get All Employee Types",
    description="Retrieve a list of all employee types.",
    responses={
        200: get_api_response_serializer(EmployeeTypeSerializer, many=True, name="EmployeeTypeListResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def get_all_employee_types(request):
    try:
        result = employee_type_service.get_all_employee_types()
        return ApiResponse(status.HTTP_200_OK, "Employee type fetched successfully", result)
    except Exception as e:
        logger.error(f"get_all_employee_types view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e), {})


@extend_schema(
    summary="Get Employee Type by ID",
    description="Retrieve details of an employee type by ID.",
    parameters=[
        OpenApiParameter(name="id", description="Employee Type ID", required=True, type=int, location=OpenApiParameter.PATH)
    ],
    responses={
        200: get_api_response_serializer(EmployeeTypeSerializer, name="EmployeeTypeResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def get_employee_type(request, id):
    try:
        type_id = int(id)
        result = employee_type_service.get_employee_type(type_id)
        return ApiResponse(status.HTTP_200_OK, "Employee type fetched successfully", result)
    except Exception as e:
        logger.error(f"get_employee_type view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e), {})


@extend_schema(
    summary="Create Employee Type",
    description="Create a new employee type.",
    request=EmployeeTypeSerializer,
    responses={
        201: get_api_response_serializer(name="EmployeeTypeCreatedResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
def create_employee_type(request):
    try:
        employee_type_service.create_employee_type(request.data)
        return ApiResponse(status.HTTP_201_CREATED, "Employee type created successfully", "")
    except Exception as e:
        logger.error(f"create_employee_type view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e), {})


@extend_schema(
    summary="Update Employee Type",
    description="Update an existing employee type by ID.",
    parameters=[
        OpenApiParameter(name="id", description="Employee Type ID", required=True, type=int, location=OpenApiParameter.PATH)
    ],
    request=EmployeeTypeSerializer,
    responses={
        200: get_api_response_serializer(name="EmployeeTypeUpdatedResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
def update_employee_type(request, id):
    try:
        type_id = int(id)
        employee_type_service.update_employee_type(type_id, request.data)
        return ApiResponse(status.HTTP_200_OK, "Employee type updated successfully", "")
    except Exception as e:
        logger.error(f"update_employee_type view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e), {})


@extend_schema(
    summary="Delete Employee Type",
    description="Delete an existing employee type by ID.",
    parameters=[
        OpenApiParameter(name="id", description="Employee Type ID", required=True, type=int, location=OpenApiParameter.PATH)
    ],
    responses={
        200: get_api_response_serializer(name="EmployeeTypeDeletedResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
def delete_employee_type(request, id):
    try:
        type_id = int(id)
        employee_type_service.delete_employee_type(type_id)
        return ApiResponse(status.HTTP_200_OK, "Employee type deleted successfully", "")
    except Exception as e:
        logger.error(f"delete_employee_type view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e), {})

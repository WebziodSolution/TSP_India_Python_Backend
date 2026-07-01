import logging
from rest_framework.decorators import api_view, authentication_classes
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter
from common.response.api_response import ApiResponse
from common.auth.authentication import JWTAuthentication
from common.serializers import EmployeeleavemasterSerializer
from common.swagger_utils import get_api_response_serializer
from .service import EmployeeLeaveMasterService

logger = logging.getLogger(__name__)
elm_service = EmployeeLeaveMasterService()

@extend_schema(
    summary="Get All Employee Leave Masters",
    description="Retrieve leave master details of all employees associated with a company ID.",
    parameters=[
        OpenApiParameter(name="companyId", description="Company ID", required=True, type=int, location=OpenApiParameter.PATH)
    ],
    responses={
        200: get_api_response_serializer(EmployeeleavemasterSerializer, many=True, name="EmployeeLeaveMastersListResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def get_all_employee_leave_masters(request, companyId):
    try:
        comp_id = int(companyId)
        result = elm_service.get_all_employee_leave_masters(comp_id)
        return ApiResponse(status.HTTP_200_OK, "Fetch employee leave master details successfully", result)
    except Exception as e:
        logger.error(f"get_all_employee_leave_masters view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Fail to fetch employee leave master details", {})


@extend_schema(
    summary="Get Employee Leave Masters by Employee ID",
    description="Retrieve all leave master details associated with a specific employee ID.",
    parameters=[
        OpenApiParameter(name="employeeId", description="Employee ID", required=True, type=int, location=OpenApiParameter.PATH)
    ],
    responses={
        200: get_api_response_serializer(EmployeeleavemasterSerializer, many=True, name="EmployeeLeaveMastersByEmployeeResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def get_employee_leave_masters_by_employee(request, employeeId):
    try:
        emp_id = int(employeeId)
        result = elm_service.get_employee_leave_masters_by_employee(emp_id)
        return ApiResponse(status.HTTP_200_OK, "Fetch employee leave master details successfully", result)
    except Exception as e:
        logger.error(f"get_employee_leave_masters_by_employee view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Fail to fetch employee leave master details", {})


@extend_schema(
    summary="Get Employee Leave Master by ID",
    description="Retrieve details of an employee leave master record by ID.",
    parameters=[
        OpenApiParameter(name="id", description="Employee Leave Master ID", required=True, type=int, location=OpenApiParameter.PATH)
    ],
    responses={
        200: get_api_response_serializer(EmployeeleavemasterSerializer, name="EmployeeLeaveMasterResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def get_employee_leave_master(request, id):
    try:
        elm_id = int(id)
        result = elm_service.get_employee_leave_master(elm_id)
        return ApiResponse(status.HTTP_200_OK, "Fetch employee leave master details successfully", result)
    except Exception as e:
        logger.error(f"get_employee_leave_master view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Fail to fetch employee leave master details", {})


@extend_schema(
    summary="Create Employee Leave Master",
    description="Create a new employee leave master record.",
    request=EmployeeleavemasterSerializer,
    responses={
        201: get_api_response_serializer(name="EmployeeLeaveMasterCreatedResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
def create_employee_leave_master(request):
    try:
        elm_service.create_employee_leave_master(request.data)
        return ApiResponse(status.HTTP_201_CREATED, "Create employee leave master details successfully", "")
    except Exception as e:
        logger.error(f"create_employee_leave_master view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Fail to create employee leave master details", {})


@extend_schema(
    summary="Update Employee Leave Master",
    description="Update an existing employee leave master record by ID.",
    parameters=[
        OpenApiParameter(name="id", description="Employee Leave Master ID", required=True, type=int, location=OpenApiParameter.PATH)
    ],
    request=EmployeeleavemasterSerializer,
    responses={
        200: get_api_response_serializer(name="EmployeeLeaveMasterUpdatedResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
def update_employee_leave_master(request, id):
    try:
        elm_id = int(id)
        elm_service.update_employee_leave_master(elm_id, request.data)
        return ApiResponse(status.HTTP_200_OK, "Update employee leave master details successfully", "")
    except Exception as e:
        logger.error(f"update_employee_leave_master view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Fail to update employee leave master details", {})


@extend_schema(
    summary="Delete Employee Leave Master",
    description="Delete an existing employee leave master record by ID.",
    parameters=[
        OpenApiParameter(name="id", description="Employee Leave Master ID", required=True, type=int, location=OpenApiParameter.PATH)
    ],
    responses={
        200: get_api_response_serializer(name="EmployeeLeaveMasterDeletedResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
def delete_employee_leave_master(request, id):
    try:
        elm_id = int(id)
        elm_service.delete_employee_leave_master(elm_id)
        return ApiResponse(status.HTTP_200_OK, "Delete employee leave master details successfully", "")
    except Exception as e:
        logger.error(f"delete_employee_leave_master view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Fail to delete employee leave master details", {})

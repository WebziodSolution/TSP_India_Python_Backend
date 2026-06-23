import logging
from rest_framework.decorators import api_view, authentication_classes
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter
from common.response.api_response import ApiResponse
from common.auth.authentication import JWTAuthentication
from common.exception.exception_handler import custom_exception_handler
from common.serializers import CompanyEmployeeSerializer, EmployeeSerializer
from .service import CompanyEmployeeService
from common.swagger_utils import get_api_response_serializer

logger = logging.getLogger(__name__)
exception_handler = custom_exception_handler

employee_service = CompanyEmployeeService()

@extend_schema(
    summary="Get All Company Employees",
    description="Retrieve all employees/contractors details for a specific company.",
    parameters=[
        OpenApiParameter(name="companyId", description="Company ID", required=True, type=int, location=OpenApiParameter.PATH)
    ],
    responses={
        200: get_api_response_serializer(CompanyEmployeeSerializer, many=True, name="CompanyEmployeeList"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def get_all_employee_by_company_id(request, companyId):
    try:
        result = employee_service.get_all_employee_by_company_id(int(companyId))
        return ApiResponse(status.HTTP_200_OK, "Fetch employee details successfully", result)
    except Exception as e:
        logger.error(f"get_all_employee_by_company_id view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Fail to fetch company details", {})


@extend_schema(
    summary="Get Employee PF and PT Report",
    description="Retrieve PF and PT reports for a company's employees in a specific month.",
    parameters=[
        OpenApiParameter(name="companyId", description="Company ID", required=True, type=int, location=OpenApiParameter.QUERY),
        OpenApiParameter(name="type", description="Report Type (PF or PT)", required=True, type=str, location=OpenApiParameter.QUERY),
        OpenApiParameter(name="month", description="Month index (0-based, e.g. 5 for June)", required=True, type=str, location=OpenApiParameter.QUERY),
        OpenApiParameter(name="userTimeZone", description="User's timezone", required=True, type=str, location=OpenApiParameter.QUERY)
    ],
    responses={
        200: get_api_response_serializer(name="ReportListResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def get_employee_pf_and_pt_report(request):
    try:
        company_id = int(request.query_params.get("companyId"))
        type_str = request.query_params.get("type")
        month = request.query_params.get("month")
        user_time_zone = request.query_params.get("userTimeZone")
        
        result = employee_service.get_reports(company_id, type_str, month, user_time_zone)
        return ApiResponse(status.HTTP_200_OK, "Fetch employee details successfully", result)
    except Exception as e:
        logger.error(f"get_employee_pf_and_pt_report view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Fail to fetch company details", {})


@extend_schema(
    summary="Get All Employee Name List By Company ID",
    description="Retrieve simplified name list of all employees in a company.",
    parameters=[
        OpenApiParameter(name="companyId", description="Company ID", required=True, type=int, location=OpenApiParameter.PATH)
    ],
    responses={
        200: get_api_response_serializer(name="EmployeeSimpleNameList"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def get_all_employee_list_by_company_id(request, companyId):
    try:
        result = employee_service.get_all_employee_list_by_company_id(int(companyId))
        return ApiResponse(status.HTTP_200_OK, "Fetch employee details successfully", result)
    except Exception as e:
        logger.error(f"get_all_employee_list_by_company_id view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Fail to fetch company details", {})


@extend_schema(
    summary="Get Employee Details By ID",
    description="Retrieve details of a single employee by their ID.",
    parameters=[
        OpenApiParameter(name="id", description="Employee ID", required=True, type=int, location=OpenApiParameter.PATH)
    ],
    responses={
        200: get_api_response_serializer(CompanyEmployeeSerializer, name="EmployeeDetailsResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def get_employee(request, id):
    try:
        result = employee_service.get_employee(int(id))
        return ApiResponse(status.HTTP_200_OK, "Fetch employee details successfully", result)
    except Exception as e:
        logger.error(f"get_employee view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Fail to fetch employee details", {})


@extend_schema(
    summary="Create Employee",
    description="Create a new company employee.",
    request=CompanyEmployeeSerializer,
    responses={
        201: get_api_response_serializer(CompanyEmployeeSerializer, name="EmployeeCreatedResponse"),
        400: get_api_response_serializer(name="ValidationErrorResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
def create_employee(request):
    try:
        serializer = CompanyEmployeeSerializer(data=request.data)
        if not serializer.is_valid():
            return ApiResponse(status.HTTP_400_BAD_REQUEST, "Invalid input data", serializer.errors)
        
        result = employee_service.create_employee(serializer.validated_data)
        return ApiResponse(status.HTTP_201_CREATED, "Employee added successfully", result)
    except Exception as e:
        logger.error(f"create_employee view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e), {})


@extend_schema(
    summary="Update Employee Details",
    description="Update existing details of an employee.",
    parameters=[
        OpenApiParameter(name="id", description="Employee ID", required=True, type=int, location=OpenApiParameter.PATH)
    ],
    request=CompanyEmployeeSerializer,
    responses={
        200: get_api_response_serializer(CompanyEmployeeSerializer, name="EmployeeUpdatedResponse"),
        400: get_api_response_serializer(name="ValidationErrorResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['PUT', 'PATCH'])
@authentication_classes([JWTAuthentication])
def update_employee(request, id):
    try:
        serializer = CompanyEmployeeSerializer(data=request.data, partial=True)
        if not serializer.is_valid():
            return ApiResponse(status.HTTP_400_BAD_REQUEST, "Invalid input data", serializer.errors)
        
        result = employee_service.update_employee(int(id), serializer.validated_data)
        return ApiResponse(status.HTTP_200_OK, "Employee updated successfully", result)
    except Exception as e:
        logger.error(f"update_employee view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e), {})


@extend_schema(
    summary="Delete Employee",
    description="Delete an employee by their ID.",
    parameters=[
        OpenApiParameter(name="id", description="Employee ID", required=True, type=int, location=OpenApiParameter.PATH)
    ],
    responses={
        200: get_api_response_serializer(name="EmployeeDeletedResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
def delete_employee(request, id):
    try:
        employee_service.delete_employee(int(id))
        return ApiResponse(status.HTTP_200_OK, "Employee deleted successfully", "")
    except Exception as e:
        logger.error(f"delete_employee view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Fail to deleted employee", {})


@extend_schema(
    summary="Upload Employee Profile Image",
    description="Update or save profile image path for an employee.",
    request=get_api_response_serializer(name="UploadProfileRequest"),
    responses={
        200: get_api_response_serializer(name="UploadProfileResponse"),
        404: get_api_response_serializer(name="ProfileNotFoundResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
def upload_employee_profile(request):
    try:
        company_id = int(request.data.get("companyId"))
        employee_id = int(request.data.get("employeeId"))
        image_path = request.data.get("employee")
        
        path = employee_service.upload_employee_profile(company_id, employee_id, image_path)
        if path == "Error":
            return ApiResponse(status.HTTP_404_NOT_FOUND, "Image does not exist in the directory", "")
        return ApiResponse(status.HTTP_200_OK, "Profile image update successfully", path)
    except Exception as e:
        logger.error(f"upload_employee_profile view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Fail to update profile image", {})


@extend_schema(
    summary="Delete Employee Profile Image",
    description="Delete the profile image directory and set profileImage path to empty.",
    parameters=[
        OpenApiParameter(name="companyId", description="Company ID", required=True, type=int, location=OpenApiParameter.PATH),
        OpenApiParameter(name="employeeId", description="Employee ID", required=True, type=int, location=OpenApiParameter.PATH)
    ],
    responses={
        200: get_api_response_serializer(name="ProfileImageDeletedResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
def delete_employee_image(request, companyId, employeeId):
    try:
        success = employee_service.delete_employee_profile(int(companyId), int(employeeId))
        if success:
            return ApiResponse(status.HTTP_200_OK, "Profile image deleted successfully", "")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Profile image not found", "")
    except Exception as e:
        logger.error(f"delete_employee_image view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Fail to delete profile image", {})


@extend_schema(
    summary="Upload Employee Aadhar Image",
    description="Update or save Aadhar image path for an employee.",
    request=get_api_response_serializer(name="UploadAadharRequest"),
    responses={
        200: get_api_response_serializer(name="UploadAadharResponse"),
        404: get_api_response_serializer(name="AadharNotFoundResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
def upload_employee_aadhar_image(request):
    try:
        company_id = int(request.data.get("companyId"))
        employee_id = int(request.data.get("employeeId"))
        image_path = request.data.get("employee")
        
        path = employee_service.upload_employee_aadhar_image(company_id, employee_id, image_path)
        if path == "Error":
            return ApiResponse(status.HTTP_404_NOT_FOUND, "Image does not exist in the directory", "")
        return ApiResponse(status.HTTP_200_OK, "Aadhar image update successfully", path)
    except Exception as e:
        logger.error(f"upload_employee_aadhar_image view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Fail to update aadhar image", {})


@extend_schema(
    summary="Delete Employee Aadhar Image",
    description="Delete the Aadhar image directory and set aadharImage path to empty.",
    parameters=[
        OpenApiParameter(name="companyId", description="Company ID", required=True, type=int, location=OpenApiParameter.PATH),
        OpenApiParameter(name="employeeId", description="Employee ID", required=True, type=int, location=OpenApiParameter.PATH)
    ],
    responses={
        200: get_api_response_serializer(name="AadharImageDeletedResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
def delete_employee_aadhar_image(request, companyId, employeeId):
    try:
        success = employee_service.delete_employee_aadhar_image(int(companyId), int(employeeId))
        if success:
            return ApiResponse(status.HTTP_200_OK, "Aadhar image deleted successfully", "")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Aadhar image not found", "")
    except Exception as e:
        logger.error(f"delete_employee_aadhar_image view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Fail to delete aadhar image", {})


@extend_schema(
    summary="Create Employee From TSP Integration",
    description="Endpoint for TSP to provision/create a new employee.",
    request=EmployeeSerializer,
    responses={
        201: get_api_response_serializer(EmployeeSerializer, name="TspEmployeeCreatedResponse"),
        400: get_api_response_serializer(name="ValidationErrorResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
def create_employee_from_tsp(request):
    try:
        serializer = EmployeeSerializer(data=request.data)
        if not serializer.is_valid():
            return ApiResponse(status.HTTP_400_BAD_REQUEST, "Invalid input data", serializer.errors)
        
        result = employee_service.create_employee_from_tsp(serializer.validated_data)
        return ApiResponse(status.HTTP_201_CREATED, "Employee added successfully", result)
    except Exception as e:
        logger.error(f"create_employee_from_tsp view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e), {})


@extend_schema(
    summary="Update Employee From TSP Integration",
    description="Endpoint for TSP to update employee details.",
    parameters=[
        OpenApiParameter(name="id", description="Employee ID", required=True, type=int, location=OpenApiParameter.PATH)
    ],
    request=EmployeeSerializer,
    responses={
        200: get_api_response_serializer(EmployeeSerializer, name="TspEmployeeUpdatedResponse"),
        400: get_api_response_serializer(name="ValidationErrorResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
def update_employee_from_tsp(request, id):
    try:
        serializer = EmployeeSerializer(data=request.data, partial=True)
        if not serializer.is_valid():
            return ApiResponse(status.HTTP_400_BAD_REQUEST, "Invalid input data", serializer.errors)
        
        result = employee_service.update_employee_from_tsp(int(id), serializer.validated_data)
        return ApiResponse(status.HTTP_200_OK, "Employee updated successfully", result)
    except Exception as e:
        logger.error(f"update_employee_from_tsp view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e), {})


@extend_schema(
    summary="Get Last User ID",
    description="Retrieve the highest/latest employee ID in the system.",
    responses={
        200: get_api_response_serializer(name="LastUserIdResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def get_last_user_id(request):
    try:
        result = employee_service.get_last_user_id()
        return ApiResponse(status.HTTP_200_OK, "Last user id fetch successfully", result)
    except Exception as e:
        logger.error(f"get_last_user_id view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Fail to fetch last user id fetch", {})

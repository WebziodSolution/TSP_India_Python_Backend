import logging
from rest_framework.decorators import api_view, authentication_classes
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter
from common.response.api_response import ApiResponse
from common.auth.authentication import JWTAuthentication
from common.exception.exception_handler import custom_exception_handler
from common.serializers import WeeklyOffSerializer
from common.swagger_utils import get_api_response_serializer
from .service import WeeklyOffService

logger = logging.getLogger(__name__)
exception_handler = custom_exception_handler

weekly_off_service = WeeklyOffService()

@extend_schema(
    summary="Get All Weekly Offs By Company",
    description="Retrieve all weekly offs templates configured for a specific company.",
    parameters=[
        OpenApiParameter(name="id", description="Company ID", required=True, type=int, location=OpenApiParameter.PATH)
    ],
    responses={
        200: get_api_response_serializer(WeeklyOffSerializer, many=True, name="WeeklyOffsList"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def get_all_by_company(request, id):
    try:
        company_id = int(id)
        result = weekly_off_service.getAllByCompany(company_id)
        return ApiResponse(status.HTTP_200_OK, "Template fetched successfully", result)
    except Exception as e:
        logger.error(f"get_all_by_company view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e), {})


@extend_schema(
    summary="Get Weekly Off By ID",
    description="Retrieve specific weekly off template by its ID.",
    parameters=[
        OpenApiParameter(name="id", description="Weekly Off ID", required=True, type=int, location=OpenApiParameter.PATH)
    ],
    responses={
        200: get_api_response_serializer(WeeklyOffSerializer, name="WeeklyOffDetailsResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def get_by_id(request, id):
    try:
        week_off_id = int(id)
        result = weekly_off_service.getById(week_off_id)
        return ApiResponse(status.HTTP_200_OK, "Template fetched successfully", result)
    except Exception as e:
        logger.error(f"get_by_id view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e), {})


@extend_schema(
    summary="Assign Weekly Off to Employees",
    description="Assign a weekly off template to list of employee IDs and/or remove it from other employee IDs.",
    request=get_api_response_serializer(name="AssignEmployeesRequest"), # simplified
    responses={
        200: get_api_response_serializer(name="AssignEmployeesResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
def assign_employees(request):
    try:
        data = request.data
        week_off_id = data.get("weekOffId")
        employee_ids = data.get("employeeIds", [])
        remove_employee_ids = data.get("removeEmployeeIds", [])
        
        result = weekly_off_service.assignEmployees(employee_ids, week_off_id, remove_employee_ids)
        return ApiResponse(status.HTTP_200_OK, "Template assigned successfully", result)
    except Exception as e:
        logger.error(f"assign_employees view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e), {})


@extend_schema(
    summary="Create Weekly Off Template",
    description="Create a new weekly off template.",
    request=WeeklyOffSerializer,
    responses={
        201: get_api_response_serializer(WeeklyOffSerializer, name="WeeklyOffCreatedResponse"),
        400: get_api_response_serializer(name="ValidationError"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
def create(request):
    try:
        serializer = WeeklyOffSerializer(data=request.data)
        if not serializer.is_valid():
            return ApiResponse(status.HTTP_400_BAD_REQUEST, "Invalid input data", serializer.errors)
        
        result = weekly_off_service.create(serializer.validated_data)
        return ApiResponse(status.HTTP_201_CREATED, "Template created successfully", result)
    except Exception as e:
        logger.error(f"create weeklyOff view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e), {})


@extend_schema(
    summary="Update Weekly Off Template",
    description="Update an existing weekly off template's configurations.",
    parameters=[
        OpenApiParameter(name="id", description="Weekly Off ID", required=True, type=int, location=OpenApiParameter.PATH)
    ],
    request=WeeklyOffSerializer,
    responses={
        200: get_api_response_serializer(WeeklyOffSerializer, name="WeeklyOffUpdatedResponse"),
        400: get_api_response_serializer(name="ValidationError"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['PATCH', 'PUT'])
@authentication_classes([JWTAuthentication])
def update(request, id):
    try:
        week_off_id = int(id)
        serializer = WeeklyOffSerializer(data=request.data, partial=True)
        if not serializer.is_valid():
            return ApiResponse(status.HTTP_400_BAD_REQUEST, "Invalid input data", serializer.errors)
            
        result = weekly_off_service.update(week_off_id, serializer.validated_data)
        return ApiResponse(status.HTTP_200_OK, "Template updated successfully", result)
    except Exception as e:
        logger.error(f"update weeklyOff view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e), {})


@extend_schema(
    summary="Delete Weekly Off Template",
    description="Delete a weekly off template by ID.",
    parameters=[
        OpenApiParameter(name="id", description="Weekly Off ID", required=True, type=int, location=OpenApiParameter.PATH)
    ],
    responses={
        200: get_api_response_serializer(name="WeeklyOffDeletedResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
def delete(request, id):
    try:
        week_off_id = int(id)
        weekly_off_service.delete(week_off_id)
        return ApiResponse(status.HTTP_200_OK, "Template deleted successfully", "")
    except Exception as e:
        logger.error(f"delete weeklyOff view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e), {})


@extend_schema(
    summary="Assign Default Weekly Off Template",
    description="Set a weekly off template as default for the company, automatically assigning it to Salaried employees.",
    parameters=[
        OpenApiParameter(name="id", description="Weekly Off ID", required=True, type=int, location=OpenApiParameter.PATH)
    ],
    responses={
        200: get_api_response_serializer(name="AssignDefaultWeeklyOffResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def assign_default_template(request, id):
    try:
        week_off_id = int(id)
        weekly_off_service.assignDefaultWeeklyOff(week_off_id)
        return ApiResponse(status.HTTP_200_OK, "This template is set as default.", "")
    except Exception as e:
        logger.error(f"assign_default_template view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e), {})

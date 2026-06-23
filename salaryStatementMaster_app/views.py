import logging
from rest_framework.decorators import api_view, authentication_classes
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter
from common.response.api_response import ApiResponse
from common.auth.authentication import JWTAuthentication
from common.exception.exception_handler import custom_exception_handler
from common.serializers.salarystatementmaster.salarystatementmaster_serializer import SalaryStatementMasterSerializer
from common.swagger_utils import get_api_response_serializer
from .service import SalaryStatementMasterService

logger = logging.getLogger(__name__)
exception_handler = custom_exception_handler

service = SalaryStatementMasterService()

@extend_schema(
    summary="Get All Statement Masters",
    description="Retrieve all salary statement masters for a company ID.",
    operation_id="get_all_statement_masters",
    parameters=[
        OpenApiParameter(name="id", description="Company ID", required=True, type=str, location=OpenApiParameter.PATH)
    ],
    responses={
        200: get_api_response_serializer(SalaryStatementMasterSerializer, many=True, name="SalaryStatementMasterList"),
        500: get_api_response_serializer(name="SalaryStatementMasterErrorResponse")
    }
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def get_all_statement_masters(request, id):
    try:
        company_id = int(id)
        result = service.getAllSalaryStatementMasters(company_id)
        return ApiResponse(status.HTTP_200_OK, "Fetch salary statement successfully", result)
    except Exception as e:
        logger.error(f"get_all_statement_masters view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Fail to fetch salary statement", {})


@extend_schema(
    summary="Get Statement Masters by Month and Year",
    description="Retrieve salary statement master by company ID, month, and year.",
    operation_id="get_statement_masters_by_month_and_year",
    parameters=[
        OpenApiParameter(name="companyId", description="Company ID", required=False, type=int, location=OpenApiParameter.QUERY),
        OpenApiParameter(name="month", description="Month", required=False, type=int, location=OpenApiParameter.QUERY),
        OpenApiParameter(name="year", description="Year", required=False, type=int, location=OpenApiParameter.QUERY),
    ],
    responses={
        200: get_api_response_serializer(SalaryStatementMasterSerializer, name="SalaryStatementMasterByMonthYear"),
        500: get_api_response_serializer(name="SalaryStatementMasterByMonthYearErrorResponse")
    }
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def get_statement_masters_by_month_and_year(request):
    try:
        company_id_str = request.query_params.get("companyId")
        month_str = request.query_params.get("month")
        year_str = request.query_params.get("year")

        company_id = int(company_id_str) if company_id_str else None
        month = int(month_str) if month_str else None
        year = int(year_str) if year_str else None

        result = service.getSalaryStatementMastersByMonthAndYear(company_id, month, year)
        return ApiResponse(status.HTTP_200_OK, "Fetch salary statement successfully", result)
    except Exception as e:
        logger.error(f"get_statement_masters_by_month_and_year view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Fail to fetch salary statement", {})


@extend_schema(
    summary="Get Salary Statement Master By ID",
    description="Retrieve a single salary statement master by its primary key ID.",
    operation_id="get_salary_statement_master_by_id",
    parameters=[
        OpenApiParameter(name="id", description="Salary Statement Master ID", required=True, type=str, location=OpenApiParameter.PATH)
    ],
    responses={
        200: get_api_response_serializer(SalaryStatementMasterSerializer, name="SalaryStatementMasterDetail"),
        500: get_api_response_serializer(name="SalaryStatementMasterDetailErrorResponse")
    }
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def get_salary_statement_master_by_id(request, id):
    try:
        master_id = int(id)
        result = service.getSalaryStatementMasterById(master_id)
        return ApiResponse(status.HTTP_200_OK, "Fetch salary statement successfully", result)
    except Exception as e:
        logger.error(f"get_salary_statement_master_by_id view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Fail to fetch salary statement", {})


@extend_schema(
    summary="Create Salary Statement Master",
    description="Create a new salary statement master.",
    operation_id="create_salary_statement_master",
    request=SalaryStatementMasterSerializer,
    responses={
        201: get_api_response_serializer(SalaryStatementMasterSerializer, name="SalaryStatementMasterCreate"),
        500: get_api_response_serializer(name="SalaryStatementMasterCreateErrorResponse")
    }
)
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
def create_salary_statement_master(request):
    try:
        serializer = SalaryStatementMasterSerializer(data=request.data)
        if serializer.is_valid():
            result = service.createSalaryStatementMaster(serializer.validated_data)
            return ApiResponse(status.HTTP_201_CREATED, "Salary statement added successfully", result)
        else:
            return ApiResponse(status.HTTP_400_BAD_REQUEST, "Invalid request data", serializer.errors)
    except Exception as e:
        logger.error(f"create_salary_statement_master view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Fail to add salary statement", {})


@extend_schema(
    summary="Update Salary Statement Master",
    description="Update an existing salary statement master by ID.",
    operation_id="update_salary_statement_master",
    parameters=[
        OpenApiParameter(name="id", description="Salary Statement Master ID", required=True, type=str, location=OpenApiParameter.PATH)
    ],
    request=SalaryStatementMasterSerializer,
    responses={
        200: get_api_response_serializer(SalaryStatementMasterSerializer, name="SalaryStatementMasterUpdate"),
        500: get_api_response_serializer(name="SalaryStatementMasterUpdateErrorResponse")
    }
)
@api_view(['PATCH'])
@authentication_classes([JWTAuthentication])
def update_salary_statement_master(request, id):
    try:
        master_id = int(id)
        serializer = SalaryStatementMasterSerializer(data=request.data)
        if serializer.is_valid():
            result = service.updateSalaryStatementMaster(master_id, serializer.validated_data)
            return ApiResponse(status.HTTP_200_OK, "Salary statement updated successfully", result)
        else:
            return ApiResponse(status.HTTP_400_BAD_REQUEST, "Invalid request data", serializer.errors)
    except Exception as e:
        logger.error(f"update_salary_statement_master view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Fail to updated salary statement", {})


@extend_schema(
    summary="Delete Salary Statement Master",
    description="Delete a salary statement master by ID.",
    operation_id="delete_salary_statement_master",
    parameters=[
        OpenApiParameter(name="id", description="Salary Statement Master ID", required=True, type=str, location=OpenApiParameter.PATH)
    ],
    responses={
        200: get_api_response_serializer(name="SalaryStatementMasterDeleteSuccessResponse"),
        500: get_api_response_serializer(name="SalaryStatementMasterDeleteErrorResponse")
    }
)
@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
def delete_salary_statement_master(request, id):
    try:
        master_id = int(id)
        service.deleteSalaryStatementMaster(master_id)
        return ApiResponse(status.HTTP_200_OK, "Salary statement deleted successfully", {})
    except Exception as e:
        logger.error(f"delete_salary_statement_master view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Fail to delete salary statement", {})

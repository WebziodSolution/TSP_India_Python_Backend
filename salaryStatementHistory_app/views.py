import logging
from rest_framework.decorators import api_view, authentication_classes
from rest_framework import status, serializers
from drf_spectacular.utils import extend_schema, OpenApiParameter
from common.response.api_response import ApiResponse
from common.auth.authentication import JWTAuthentication
from common.exception.exception_handler import custom_exception_handler
from common.serializers.salarystatementhistory.salarystatementhistory_serializer import SalaryStatementHistorySerializer
from common.swagger_utils import get_api_response_serializer
from .service import SalaryStatementHistoryService

logger = logging.getLogger(__name__)
exception_handler = custom_exception_handler

service = SalaryStatementHistoryService()

class SalaryStatementHistoryFilterRequestSerializer(serializers.Serializer):
    employeeIds = serializers.ListField(child=serializers.IntegerField(), required=False, allow_empty=True)
    departmentIds = serializers.ListField(child=serializers.IntegerField(), required=False, allow_empty=True)
    month = serializers.ListField(child=serializers.CharField(), required=False, allow_empty=True)
    companyId = serializers.IntegerField(required=True)

class SalaryStatementHistoryGroupSerializer(serializers.Serializer):
    month = serializers.CharField()
    data = SalaryStatementHistorySerializer(many=True)

@extend_schema(
    summary="Filter Salary Statement History",
    description="Retrieve filtered list of salary statement histories grouped by month.",
    operation_id="filter_salary_statement_history",
    request=SalaryStatementHistoryFilterRequestSerializer,
    responses={
        200: get_api_response_serializer(SalaryStatementHistoryGroupSerializer, many=True, name="SalaryStatementHistoryFilter"),
        500: get_api_response_serializer(name="SalaryStatementHistoryFilterErrorResponse")
    }
)
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
def filter_salary_statement_history(request):
    try:
        data = request.data
        employee_ids = data.get("employeeIds", [])
        department_ids = data.get("departmentIds", [])
        months = data.get("month", [])
        company_id = int(data.get("companyId")) if data.get("companyId") is not None else None

        result = service.filterSalaryStatementHistory(employee_ids, department_ids, months, company_id)
        return ApiResponse(status.HTTP_200_OK, "Fetch salary data successfully", result)
    except Exception as e:
        logger.error(f"filter_salary_statement_history view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Fail to fetch salary data", {})


@extend_schema(
    summary="Get Salary Statement History By ID",
    description="Retrieve a single salary statement history by its primary key ID.",
    operation_id="get_salary_statement_history",
    parameters=[
        OpenApiParameter(name="id", description="Salary Statement History ID", required=True, type=str, location=OpenApiParameter.PATH)
    ],
    responses={
        200: get_api_response_serializer(SalaryStatementHistorySerializer, name="SalaryStatementHistoryDetail"),
        500: get_api_response_serializer(name="SalaryStatementHistoryDetailErrorResponse")
    }
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def get_salary_statement_history(request, id):
    try:
        history_id = int(id)
        result = service.getSalaryStatementHistory(history_id)
        return ApiResponse(status.HTTP_200_OK, "Fetch salary data successfully", result)
    except Exception as e:
        logger.error(f"get_salary_statement_history view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Fail to fetch salary data", {})


@extend_schema(
    summary="Add Salary Statement History Records",
    description="Add a list of salary statement history records.",
    operation_id="add_salary_statement_history",
    request=SalaryStatementHistorySerializer(many=True),
    responses={
        201: get_api_response_serializer(name="SalaryStatementHistoryAddSuccess"),
        500: get_api_response_serializer(name="SalaryStatementHistoryAddErrorResponse")
    }
)
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
def add_salary_statement(request):
    try:
        logger.info(f"add_salary_statement request data: {request.data}")
        serializer = SalaryStatementHistorySerializer(data=request.data, many=True)
        if serializer.is_valid():
            result = service.addSalaryStatement(serializer.validated_data)
            return ApiResponse(status.HTTP_201_CREATED, "Salary data added successfully", result)
        else:
            logger.error(f"add_salary_statement validation error: {serializer.errors}")
            return ApiResponse(status.HTTP_400_BAD_REQUEST, "Invalid request data", serializer.errors)
    except Exception as e:
        logger.error(f"add_salary_statement view error: {e}")
        # Return e.getMessage() / str(e) to match Java error response format
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e), {})


@extend_schema(
    summary="Update Salary Statement History Record By ID",
    description="Update an existing salary statement history record by ID.",
    operation_id="update_salary_statement_history",
    parameters=[
        OpenApiParameter(name="id", description="Salary Statement History ID", required=True, type=str, location=OpenApiParameter.PATH)
    ],
    request=SalaryStatementHistorySerializer,
    responses={
        200: get_api_response_serializer(SalaryStatementHistorySerializer, name="SalaryStatementHistoryUpdate"),
        500: get_api_response_serializer(name="SalaryStatementHistoryUpdateErrorResponse")
    }
)
@api_view(['PATCH'])
@authentication_classes([JWTAuthentication])
def update_salary_statement(request, id):
    try:
        history_id = int(id)
        logger.info(f"update_salary_statement request data: {request.data}")
        serializer = SalaryStatementHistorySerializer(data=request.data)
        if serializer.is_valid():
            result = service.updateSalaryStatement(history_id, serializer.validated_data)
            return ApiResponse(status.HTTP_200_OK, "Salary data updated successfully", result)
        else:
            logger.error(f"update_salary_statement validation error: {serializer.errors}")
            return ApiResponse(status.HTTP_400_BAD_REQUEST, "Invalid request data", serializer.errors)
    except Exception as e:
        logger.error(f"update_salary_statement view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Fail to update salary data", {})


@extend_schema(
    summary="Delete Salary Statement History Record By ID",
    description="Delete an existing salary statement history record by ID.",
    operation_id="delete_salary_statement_history",
    parameters=[
        OpenApiParameter(name="id", description="Salary Statement History ID", required=True, type=str, location=OpenApiParameter.PATH)
    ],
    responses={
        200: get_api_response_serializer(name="SalaryStatementHistoryDeleteSuccessResponse"),
        500: get_api_response_serializer(name="SalaryStatementHistoryDeleteErrorResponse")
    }
)
@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
def delete_salary_statement(request, id):
    try:
        history_id = int(id)
        service.deleteSalaryStatement(history_id)
        return ApiResponse(status.HTTP_200_OK, "Salary data deleted successfully", {})
    except Exception as e:
        logger.error(f"delete_salary_statement view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Fail to delete salary data", {})

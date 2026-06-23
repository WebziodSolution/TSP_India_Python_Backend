import logging
from rest_framework.decorators import api_view, authentication_classes
from rest_framework import status
from drf_spectacular.utils import extend_schema
from common.response.api_response import ApiResponse
from common.auth.authentication import JWTAuthentication
from common.exception.exception_handler import custom_exception_handler
from common.serializers import SalaryStatementRequestSerializer, EmployeeSalaryStatementSerializer
from common.swagger_utils import get_api_response_serializer
from .service import EmployeeSalaryStatementService

logger = logging.getLogger(__name__)
exception_handler = custom_exception_handler

employee_salary_statement_service = EmployeeSalaryStatementService()

@extend_schema(
    summary="Get Employee Salary Statements",
    description="Retrieve employee salary statements based on employee IDs, department IDs, company ID, and date range.",
    request=SalaryStatementRequestSerializer,
    responses={
        200: get_api_response_serializer(EmployeeSalaryStatementSerializer, many=True, name="SalaryStatementsResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
def get_employee_salary_statements(request):
    try:
        serializer = SalaryStatementRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return ApiResponse(status.HTTP_400_BAD_REQUEST, "Invalid request body", serializer.errors)
            
        result = employee_salary_statement_service.get_employee_salary_statements(serializer.validated_data)
        response_serializer = EmployeeSalaryStatementSerializer(result, many=True)
        return ApiResponse(status.HTTP_200_OK, "Fetch statement successfully", response_serializer.data)
    except Exception as e:
        logger.error(f"get_employee_salary_statements view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Fail to fetch statement", None)

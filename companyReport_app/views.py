import logging
from rest_framework.decorators import api_view, authentication_classes
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter
from common.response.api_response import ApiResponse
from common.auth.authentication import JWTAuthentication
from common.exception.exception_handler import custom_exception_handler
from common.serializers.companyreportdto.companyreportresponse_serializer import CompanyReportResponseSerializer
from common.swagger_utils import get_api_response_serializer
from .service import CompanyReportService

logger = logging.getLogger(__name__)
exception_handler = custom_exception_handler

company_report_service = CompanyReportService()

@extend_schema(
    summary="Get Filtered Companies",
    description="Retrieve paginated list of companies filtered by registration dates, employee counts and timezone.",
    parameters=[
        OpenApiParameter(name="startDate", description="Start date (e.g., '01/01/2026')", required=False, type=str),
        OpenApiParameter(name="endDate", description="End date (e.g., '31/12/2026')", required=False, type=str),
        OpenApiParameter(name="min", description="Min employee count", required=False, type=int),
        OpenApiParameter(name="max", description="Max employee count", required=False, type=int),
        OpenApiParameter(name="timeZone", description="Timezone (e.g., 'Asia/Kolkata')", required=False, type=str),
        OpenApiParameter(name="page", description="Page index (0-indexed)", required=False, type=int),
        OpenApiParameter(name="size", description="Page size", required=False, type=int)
    ],
    responses={
        200: get_api_response_serializer(CompanyReportResponseSerializer, name="CompanyReportResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def get_filtered_companies(request):
    try:
        start_date = request.query_params.get("startDate")
        end_date = request.query_params.get("endDate")
        
        min_val_str = request.query_params.get("min")
        max_val_str = request.query_params.get("max")
        time_zone = request.query_params.get("timeZone")
        
        page_str = request.query_params.get("page")
        size_str = request.query_params.get("size")
        
        min_val = int(min_val_str) if min_val_str else None
        max_val = int(max_val_str) if max_val_str else None
        
        page = int(page_str) if page_str else 0
        size = int(size_str) if size_str else 10
        
        result = company_report_service.getCompanies(start_date, end_date, min_val, max_val, page, size, time_zone)
        return ApiResponse(status.HTTP_200_OK, "Companies fetched successfully", result)
    except Exception as e:
        logger.error(f"get_filtered_companies view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to fetch companies", {})

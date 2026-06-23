import logging
from rest_framework.decorators import api_view, authentication_classes
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter
from common.response.api_response import ApiResponse
from common.auth.authentication import JWTAuthentication
from common.serializers import HolidayTemplatesSerializer
from common.swagger_utils import get_api_response_serializer
from .service import HolidayTemplatesService

logger = logging.getLogger(__name__)
templates_service = HolidayTemplatesService()

@extend_schema(
    summary="Get All Holiday Templates by Company",
    description="Retrieve all holiday templates associated with a company ID.",
    parameters=[
        OpenApiParameter(name="id", description="Company ID", required=True, type=int, location=OpenApiParameter.PATH)
    ],
    responses={
        200: get_api_response_serializer(HolidayTemplatesSerializer, many=True, name="HolidayTemplatesListResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def get_all_holiday_templates_by_company_id(request, id):
    try:
        company_id = int(id)
        result = templates_service.get_all_holiday_templates_by_company_id(company_id)
        return ApiResponse(status.HTTP_200_OK, "Holiday templates fetched successfully", result)
    except Exception as e:
        logger.error(f"get_all_holiday_templates_by_company_id view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e), {})


@extend_schema(
    summary="Get Holiday Template by ID",
    description="Retrieve holiday template details by ID.",
    parameters=[
        OpenApiParameter(name="id", description="Template ID", required=True, type=int, location=OpenApiParameter.PATH)
    ],
    responses={
        200: get_api_response_serializer(HolidayTemplatesSerializer, name="HolidayTemplatesResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def get_holiday_template(request, id):
    try:
        template_id = int(id)
        result = templates_service.get_holiday_template_by_id(template_id)
        return ApiResponse(status.HTTP_200_OK, "Holiday template fetched successfully", result)
    except Exception as e:
        logger.error(f"get_holiday_template view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e), {})


@extend_schema(
    summary="Create Holiday Template",
    description="Create a new holiday template.",
    request=HolidayTemplatesSerializer,
    responses={
        201: get_api_response_serializer(HolidayTemplatesSerializer, name="HolidayTemplatesCreatedResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
def create_holiday_template(request):
    try:
        data = request.data.copy() if hasattr(request.data, 'copy') else request.data
        data["createdBy"] = request.user_id
        result = templates_service.create_holiday_template(data)
        return ApiResponse(status.HTTP_201_CREATED, "Holiday template created successfully", result)
    except Exception as e:
        logger.error(f"create_holiday_template view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e), {})


@extend_schema(
    summary="Update Holiday Template",
    description="Update existing holiday template details by ID.",
    parameters=[
        OpenApiParameter(name="id", description="Template ID", required=True, type=int, location=OpenApiParameter.PATH)
    ],
    request=HolidayTemplatesSerializer,
    responses={
        200: get_api_response_serializer(HolidayTemplatesSerializer, name="HolidayTemplatesUpdatedResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['PATCH'])
@authentication_classes([JWTAuthentication])
def update_holiday_template(request, id):
    try:
        template_id = int(id)
        data = request.data.copy() if hasattr(request.data, 'copy') else request.data
        data["createdBy"] = request.user_id
        result = templates_service.update_holiday_template(template_id, data)
        return ApiResponse(status.HTTP_200_OK, "Holiday template updated successfully", result)
    except Exception as e:
        logger.error(f"update_holiday_template view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e), {})


@extend_schema(
    summary="Delete Holiday Template",
    description="Delete holiday template record by ID.",
    parameters=[
        OpenApiParameter(name="id", description="Template ID", required=True, type=int, location=OpenApiParameter.PATH)
    ],
    responses={
        200: get_api_response_serializer(name="HolidayTemplatesDeletedResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
def delete_holiday_template(request, id):
    try:
        template_id = int(id)
        templates_service.delete_holiday_template(template_id)
        return ApiResponse(status.HTTP_200_OK, "Holiday template deleted successfully", "")
    except Exception as e:
        logger.error(f"delete_holiday_template view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e), {})


@extend_schema(
    summary="Assign Employees to Holiday Template",
    description="Assign or remove list of employees on a holiday template.",
    request=get_api_response_serializer(name="AssignEmployeesRequest"),
    responses={
        200: get_api_response_serializer(name="AssignEmployeesResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
def assign_employees(request):
    try:
        template_id = request.data.get("id")
        employee_ids = request.data.get("employeeIds", [])
        remove_employee_ids = request.data.get("removeEmployeeIds", [])
        result = templates_service.assign_employees(template_id, employee_ids, remove_employee_ids)
        return ApiResponse(status.HTTP_200_OK, "Template assigned successfully", result)
    except Exception as e:
        logger.error(f"assign_employees view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e), {})

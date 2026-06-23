import logging
from django.http import HttpResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter
from common.response.api_response import ApiResponse
from common.auth.authentication import JWTAuthentication
from common.exception.exception_handler import custom_exception_handler
from common.serializers import UserInOutSerializer, BulkUserInOutSerializer
from common.swagger_utils import get_api_response_serializer
from .service import UserInOutService

logger = logging.getLogger(__name__)
exception_handler = custom_exception_handler

user_in_out_service = UserInOutService()

@extend_schema(
    summary="Get In-Out Report",
    description="Retrieve clock in/out details for specified users and date range.",
    parameters=[
        OpenApiParameter(name="userIds", description="List of user IDs", required=False, type=int, many=True, location=OpenApiParameter.QUERY),
        OpenApiParameter(name="startDate", description="Start date (dd/MM/yyyy)", required=False, type=str, location=OpenApiParameter.QUERY),
        OpenApiParameter(name="endDate", description="End date (dd/MM/yyyy)", required=False, type=str, location=OpenApiParameter.QUERY),
        OpenApiParameter(name="timeZone", description="TimeZone", required=False, type=str, location=OpenApiParameter.QUERY),
        OpenApiParameter(name="companyId", description="Company ID", required=False, type=str, location=OpenApiParameter.QUERY),
    ],
    responses={
        200: get_api_response_serializer(name="InOutReportResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def get_report(request):
    try:
        user_ids_raw = request.query_params.getlist("userIds")
        user_ids = []
        for val in user_ids_raw:
            if "," in val:
                user_ids.extend([int(x.strip()) for x in val.split(",") if x.strip()])
            else:
                user_ids.append(int(val))

        start_date = request.query_params.get("startDate")
        end_date = request.query_params.get("endDate")
        time_zone = request.query_params.get("timeZone")
        company_id_raw = request.query_params.get("companyId")
        company_id = int(company_id_raw) if company_id_raw else None

        res_body = user_in_out_service.get_time_inout_report(user_ids, start_date, end_date, time_zone, company_id)
        return ApiResponse(status.HTTP_200_OK, "InOut's Report fetched successfully", res_body)
    except Exception as e:
        logger.error(f"get_report view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to Fetch InOut's Report", {"error": str(e)})

@extend_schema(
    summary="Generate Excel In-Out Report",
    description="Generate and download Excel spreadsheet report of users' clock entries.",
    parameters=[
        OpenApiParameter(name="userIds", description="List of user IDs", required=False, type=int, many=True, location=OpenApiParameter.QUERY),
        OpenApiParameter(name="startDate", description="Start date (dd/MM/yyyy)", required=False, type=str, location=OpenApiParameter.QUERY),
        OpenApiParameter(name="endDate", description="End date (dd/MM/yyyy)", required=False, type=str, location=OpenApiParameter.QUERY),
        OpenApiParameter(name="timeZone", description="TimeZone", required=False, type=str, location=OpenApiParameter.QUERY),
        OpenApiParameter(name="companyId", description="Company ID", required=False, type=int, location=OpenApiParameter.QUERY),
    ],
    responses={
        200: get_api_response_serializer(name="ExcelResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def generate_excel_report(request):
    try:
        user_ids_raw = request.query_params.getlist("userIds")
        user_ids = []
        for val in user_ids_raw:
            if "," in val:
                user_ids.extend([int(x.strip()) for x in val.split(",") if x.strip()])
            else:
                user_ids.append(int(val))

        start_date = request.query_params.get("startDate")
        end_date = request.query_params.get("endDate")
        time_zone = request.query_params.get("timeZone")
        company_id_raw = request.query_params.get("companyId")
        company_id = int(company_id_raw) if company_id_raw else None

        report_data = user_in_out_service.get_time_inout_report(user_ids, start_date, end_date, time_zone, company_id)
        workbook = user_in_out_service.generate_excel_report(report_data, start_date, end_date, time_zone)

        response = HttpResponse(content_type='application/octet-stream')
        response['Content-Disposition'] = 'attachment; filename=InOutReport.xlsx'
        workbook.save(response)
        return response
    except Exception as e:
        logger.error(f"generate_excel_report view error: {e}")
        return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@extend_schema(
    summary="Get Dashboard Data",
    description="Retrieve counts of checked-in/out users and total employee count for a company.",
    parameters=[
        OpenApiParameter(name="companyId", description="Company ID", required=True, type=int, location=OpenApiParameter.PATH)
    ],
    responses={
        200: get_api_response_serializer(name="DashboardCountsResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def get_dashboard_data(request, companyId):
    try:
        result = user_in_out_service.dashboard_counts(int(companyId))
        return ApiResponse(status.HTTP_200_OK, "Current In-Users fetched successfully", result)
    except Exception as e:
        logger.error(f"get_dashboard_data view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Fail to get userInOut", {})

@extend_schema(
    summary="Get User Last In-Out",
    description="Retrieve the very last check-in/out record for a specific employee.",
    parameters=[
        OpenApiParameter(name="userId", description="User ID", required=True, type=int, location=OpenApiParameter.PATH)
    ],
    responses={
        200: get_api_response_serializer(UserInOutSerializer, name="UserLastInOutResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def get_user_last_inout(request, userId):
    try:
        result = user_in_out_service.get_user_last_inout(int(userId))
        return ApiResponse(status.HTTP_200_OK, "User fetched successfully", result)
    except Exception as e:
        logger.error(f"get_user_last_inout view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Fail to get userInOut", {})

@extend_schema(
    summary="Get All In-Out Records",
    description="Retrieve raw list of all clock-in/out records matching filter criteria.",
    parameters=[
        OpenApiParameter(name="userIds", description="List of user IDs", required=False, type=int, many=True, location=OpenApiParameter.QUERY),
        OpenApiParameter(name="startDate", description="Start date (dd/MM/yyyy)", required=False, type=str, location=OpenApiParameter.QUERY),
        OpenApiParameter(name="endDate", description="End date (dd/MM/yyyy)", required=False, type=str, location=OpenApiParameter.QUERY),
        OpenApiParameter(name="timeZone", description="TimeZone", required=False, type=str, location=OpenApiParameter.QUERY),
        OpenApiParameter(name="locationIds", description="List of location IDs", required=False, type=int, many=True, location=OpenApiParameter.QUERY),
        OpenApiParameter(name="departmentIds", description="List of department IDs", required=False, type=int, many=True, location=OpenApiParameter.QUERY),
        OpenApiParameter(name="companyId", description="Company ID", required=False, type=int, location=OpenApiParameter.QUERY),
    ],
    responses={
        200: get_api_response_serializer(UserInOutSerializer, many=True, name="AllRecordsList"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def get_all_records(request):
    try:
        user_ids_raw = request.query_params.getlist("userIds")
        user_ids = []
        for val in user_ids_raw:
            if "," in val:
                user_ids.extend([int(x.strip()) for x in val.split(",") if x.strip()])
            else:
                user_ids.append(int(val))

        location_ids_raw = request.query_params.getlist("locationIds")
        location_ids = []
        for val in location_ids_raw:
            if "," in val:
                location_ids.extend([int(x.strip()) for x in val.split(",") if x.strip()])
            else:
                location_ids.append(int(val))

        dept_ids_raw = request.query_params.getlist("departmentIds")
        dept_ids = []
        for val in dept_ids_raw:
            if "," in val:
                dept_ids.extend([int(x.strip()) for x in val.split(",") if x.strip()])
            else:
                dept_ids.append(int(val))

        start_date = request.query_params.get("startDate")
        end_date = request.query_params.get("endDate")
        time_zone = request.query_params.get("timeZone")
        company_id_raw = request.query_params.get("companyId")
        company_id = int(company_id_raw) if company_id_raw else None

        result = user_in_out_service.get_all_entries_by_user_id(user_ids, start_date, end_date, time_zone, location_ids, dept_ids, company_id)
        return ApiResponse(status.HTTP_200_OK, "UserInOut fetched successfully", result)
    except Exception as e:
        logger.error(f"get_all_records view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Fail to get userInOut", {})

@extend_schema(
    summary="Get All In-Out Records Grouped By User",
    description="Retrieve all clock entries grouped chronologically by user with calculated present/absent stats.",
    parameters=[
        OpenApiParameter(name="userIds", description="List of user IDs", required=False, type=int, many=True, location=OpenApiParameter.QUERY),
        OpenApiParameter(name="startDate", description="Start date (dd/MM/yyyy)", required=False, type=str, location=OpenApiParameter.QUERY),
        OpenApiParameter(name="endDate", description="End date (dd/MM/yyyy)", required=False, type=str, location=OpenApiParameter.QUERY),
        OpenApiParameter(name="timeZone", description="TimeZone", required=False, type=str, location=OpenApiParameter.QUERY),
        OpenApiParameter(name="locationIds", description="List of location IDs", required=False, type=int, many=True, location=OpenApiParameter.QUERY),
        OpenApiParameter(name="departmentIds", description="List of department IDs", required=False, type=int, many=True, location=OpenApiParameter.QUERY),
        OpenApiParameter(name="companyId", description="Company ID", required=False, type=int, location=OpenApiParameter.QUERY),
    ],
    responses={
        200: get_api_response_serializer(name="AllRecordsGroupedByUserResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def get_all_records_grouped_by_user(request):
    try:
        user_ids_raw = request.query_params.getlist("userIds")
        user_ids = []
        for val in user_ids_raw:
            if "," in val:
                user_ids.extend([int(x.strip()) for x in val.split(",") if x.strip()])
            else:
                user_ids.append(int(val))

        location_ids_raw = request.query_params.getlist("locationIds")
        location_ids = []
        for val in location_ids_raw:
            if "," in val:
                location_ids.extend([int(x.strip()) for x in val.split(",") if x.strip()])
            else:
                location_ids.append(int(val))

        dept_ids_raw = request.query_params.getlist("departmentIds")
        dept_ids = []
        for val in dept_ids_raw:
            if "," in val:
                dept_ids.extend([int(x.strip()) for x in val.split(",") if x.strip()])
            else:
                dept_ids.append(int(val))

        start_date = request.query_params.get("startDate")
        end_date = request.query_params.get("endDate")
        time_zone = request.query_params.get("timeZone")
        company_id_raw = request.query_params.get("companyId")
        company_id = int(company_id_raw) if company_id_raw else None

        result = user_in_out_service.get_all_entries_grouped_by_user(user_ids, start_date, end_date, time_zone, location_ids, dept_ids, company_id)
        return ApiResponse(status.HTTP_200_OK, "UserInOut fetched successfully", result)
    except Exception as e:
        logger.error(f"get_all_records_grouped_by_user view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Fail to get userInOut", {})

@extend_schema(
    summary="Get Today's Records for Logged-In User",
    description="Retrieve all check in/out entries for the currently authenticated employee today.",
    responses={
        200: get_api_response_serializer(UserInOutSerializer, many=True, name="TodayRecordsResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def get_today_records(request):
    try:
        user_id = request.user_id
        result = user_in_out_service.get_today_entries_by_user_id(int(user_id))
        return ApiResponse(status.HTTP_200_OK, "UserInOut fetched successfully", result)
    except Exception as e:
        logger.error(f"get_today_records view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Fail to get userInOut", {})

@extend_schema(
    summary="Get In-Out Record By ID",
    description="Retrieve details of a single check-in/out record by its database ID.",
    parameters=[
        OpenApiParameter(name="id", description="Record ID", required=True, type=int, location=OpenApiParameter.PATH)
    ],
    responses={
        200: get_api_response_serializer(UserInOutSerializer, name="RecordDetailResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def get_user_inout(request, id):
    try:
        result = user_in_out_service.get_user_inout(int(id))
        return ApiResponse(status.HTTP_200_OK, "UserInOut fetched successfully", result)
    except Exception as e:
        logger.error(f"get_user_inout view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Fail to get userInOut", {})

@extend_schema(
    summary="Create In-Out Record",
    description="Manually create a clock-in record for the authenticated user.",
    request=None,
    parameters=[
        OpenApiParameter(name="locationId", description="Location ID", required=False, type=str, location=OpenApiParameter.QUERY),
        OpenApiParameter(name="companyId", description="Company ID", required=False, type=str, location=OpenApiParameter.QUERY)
    ],
    responses={
        201: get_api_response_serializer(name="CreateRecordSuccess"),
        500: get_api_response_serializer(name="ErrorResponse")
    },
    operation_id="create_user_inout"
)
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
def create_user_inout(request):
    try:
        user_id = request.user_id
        location_id_raw = request.query_params.get("locationId")
        company_id_raw = request.query_params.get("companyId")

        parsed_location_id = None
        if location_id_raw and location_id_raw != "undefined" and location_id_raw.strip() != "":
            parsed_location_id = int(location_id_raw)

        parsed_company_id = None
        if company_id_raw and company_id_raw != "undefined" and company_id_raw.strip() != "":
            parsed_company_id = int(company_id_raw)

        result = user_in_out_service.create_user_inout(int(user_id), parsed_location_id, parsed_company_id)
        return ApiResponse(status.HTTP_201_CREATED, "UserInOut added successfully", result)
    except Exception as e:
        logger.error(f"create_user_inout view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Fail to create userInOut", {})

@extend_schema(
    summary="Update In-Out Record By ID",
    description="Update checkout timestamp of an in-out record using the current server datetime.",
    request=None,
    parameters=[
        OpenApiParameter(name="id", description="Record ID", required=True, type=int, location=OpenApiParameter.PATH)
    ],
    responses={
        200: get_api_response_serializer(name="UpdateSuccess"),
        500: get_api_response_serializer(name="ErrorResponse")
    },
    operation_id="update_user_inout_by_id"
)
@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
def update_user_inout_by_id(request, id):
    try:
        user_id = request.user_id
        user_in_out_service.update_user_inout_by_id(int(id), int(user_id))
        return ApiResponse(status.HTTP_200_OK, "UserInOut updated successfully", "")
    except Exception as e:
        logger.error(f"update_user_inout_by_id view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Fail to update userInOut details", {})

@extend_schema(
    summary="Update In-Out Record by Serializer DTO",
    description="Update full record details using the request payload.",
    request=UserInOutSerializer,
    responses={
        200: get_api_response_serializer(name="UpdateSuccess"),
        400: get_api_response_serializer(name="ValidationError"),
        500: get_api_response_serializer(name="ErrorResponse")
    },
    operation_id="update_user_inout_by_dto"
)
@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
def update_user_inout_by_dto(request):
    try:
        serializer = UserInOutSerializer(data=request.data)
        if not serializer.is_valid():
            return ApiResponse(status.HTTP_400_BAD_REQUEST, "Invalid input data", serializer.errors)

        user_in_out_service.update_user_inout_by_dto(serializer.validated_data)
        return ApiResponse(status.HTTP_200_OK, "UserInOut updated successfully", "")
    except Exception as e:
        logger.error(f"update_user_inout_by_dto view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Fail to update userInOut details", {})

@extend_schema(
    summary="Employee Clock In/Out Public Link",
    description="Public API to trigger clock in or clock out for an employee based on location & company ID.",
    request=None,
    parameters=[
        OpenApiParameter(name="employeeId", description="Employee/User ID", required=True, type=str, location=OpenApiParameter.QUERY),
        OpenApiParameter(name="locationId", description="Location ID", required=False, type=str, location=OpenApiParameter.QUERY),
        OpenApiParameter(name="companyId", description="Company ID", required=True, type=str, location=OpenApiParameter.QUERY)
    ],
    responses={
        200: get_api_response_serializer(name="ClockOutSuccess"),
        201: get_api_response_serializer(name="ClockInSuccess"),
        500: get_api_response_serializer(name="ErrorResponse")
    },
    operation_id="clock_in_out"
)
@api_view(['POST'])
@permission_classes([AllowAny])
def clock_in_out(request):
    try:
        employee_id = request.query_params.get("employeeId")
        location_id_raw = request.query_params.get("locationId")
        company_id = request.query_params.get("companyId")

        if not employee_id or not company_id:
            return ApiResponse(status.HTTP_400_BAD_REQUEST, "Missing employeeId or companyId", {})

        parsed_location_id = None
        if location_id_raw and location_id_raw != "undefined" and location_id_raw.strip() != "":
            parsed_location_id = int(location_id_raw)

        res = user_in_out_service.click_in_out(int(employee_id), parsed_location_id, int(company_id))
        parts = res.split(":", 1)
        res_status = parts[0]
        username = parts[1] if len(parts) > 1 else ""

        if res_status == "created":
            return ApiResponse(status.HTTP_201_CREATED, f"{username} clock in successfully", "")
        else:
            return ApiResponse(status.HTTP_200_OK, f"{username} clock out successfully", "")
    except Exception as e:
        logger.error(f"clock_in_out view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Fail to create userInOut", {})

@extend_schema(
    summary="Add Clock In/Out DTO Record",
    description="Directly add or update clock entry by serialized input payload.",
    request=UserInOutSerializer,
    responses={
        201: get_api_response_serializer(UserInOutSerializer, name="AddSuccess"),
        500: get_api_response_serializer(name="ErrorResponse")
    },
    operation_id="add_clock_in_out"
)
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
def add_clock_in_out(request):
    try:
        serializer = UserInOutSerializer(data=request.data)
        if not serializer.is_valid():
            return ApiResponse(status.HTTP_400_BAD_REQUEST, "Invalid input data", serializer.errors)

        result = user_in_out_service.add_clock_in_out(serializer.validated_data)
        return ApiResponse(status.HTTP_201_CREATED, "UserInOut added successfully", result)
    except Exception as e:
        logger.error(f"add_clock_in_out view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Fail to create userInOut", {})

@extend_schema(
    summary="Delete In-Out Record",
    description="Delete an in-out record by its primary key.",
    parameters=[
        OpenApiParameter(name="id", description="Record ID", required=True, type=int, location=OpenApiParameter.PATH)
    ],
    responses={
        200: get_api_response_serializer(name="DeleteSuccess"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
def delete_user_inout(request, id):
    try:
        user_in_out_service.delete_user_inout(int(id))
        return ApiResponse(status.HTTP_200_OK, "UserInOut deleted successfully", "")
    except Exception as e:
        logger.error(f"delete_user_inout view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Fail to delete userInOut record", {})

@extend_schema(
    summary="Bulk Create Clock In/Out Entries",
    description="Bulk add clock in/out entries for multiple users over a date range, skipping holidays and weekly-offs.",
    request=BulkUserInOutSerializer,
    responses={
        201: get_api_response_serializer(name="BulkAddSuccess"),
        400: get_api_response_serializer(name="ValidationError"),
        500: get_api_response_serializer(name="ErrorResponse")
    },
    operation_id="add_bulk_clock_in_out"
)
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
def add_bulk_clock_in_out(request):
    try:
        serializer = BulkUserInOutSerializer(data=request.data)
        if not serializer.is_valid():
            return ApiResponse(status.HTTP_400_BAD_REQUEST, "Invalid input data", serializer.errors)
        
        user_in_out_service.add_bulk_clock_in_out(serializer.validated_data)
        return ApiResponse(status.HTTP_201_CREATED, "Bulk UserInOut added successfully", "")
    except Exception as e:
        logger.error(f"add_bulk_clock_in_out view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Fail to bulk create userInOut", {"error": str(e)})


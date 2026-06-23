import logging
from rest_framework.decorators import api_view, authentication_classes
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter
from common.response.api_response import ApiResponse
from common.auth.authentication import JWTAuthentication
from common.exception.exception_handler import custom_exception_handler
from common.serializers import AttendancePenaltyRulesSerializer
from common.swagger_utils import get_api_response_serializer
from .service import AttendancePenaltyRulesService

logger = logging.getLogger(__name__)
exception_handler = custom_exception_handler

attendance_penalty_rules_service = AttendancePenaltyRulesService()

@extend_schema(
    summary="Get All Attendance Penalty Rules",
    description="Retrieve all attendance penalty rules associated with a specific company and flag.",
    parameters=[
        OpenApiParameter(name="flag", description="Flag (1 for early exit, others otherwise)", required=True, type=int, location=OpenApiParameter.PATH),
        OpenApiParameter(name="companyId", description="Company ID", required=True, type=int, location=OpenApiParameter.PATH)
    ],
    responses={
        200: get_api_response_serializer(AttendancePenaltyRulesSerializer, many=True, name="AttendancePenaltyRulesList"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def get_all_by_company_id(request, flag, companyId):
    try:
        flag_val = int(flag)
        company_id = int(companyId)
        result = attendance_penalty_rules_service.find_all_by_company_id(flag_val, company_id)
        return ApiResponse(status.HTTP_200_OK, "Fetch attendance penalty rules successfully", result)
    except Exception as e:
        logger.error(f"get_all_by_company_id view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Fail to fetch attendance penalty rules", {})


@extend_schema(
    summary="Get Attendance Penalty Rule by ID",
    description="Retrieve a single attendance penalty rule details by its ID.",
    parameters=[
        OpenApiParameter(name="id", description="Rule ID", required=True, type=int, location=OpenApiParameter.PATH)
    ],
    responses={
        200: get_api_response_serializer(AttendancePenaltyRulesSerializer, name="AttendancePenaltyRuleDetail"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def get_by_id(request, id):
    try:
        rule_id = int(id)
        result = attendance_penalty_rules_service.find_by_id(rule_id)
        return ApiResponse(status.HTTP_200_OK, "Fetch attendance rule successfully", result)
    except Exception as e:
        logger.error(f"get_by_id view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Fail to fetch attendance penalty rule", {})


@extend_schema(
    summary="Create Attendance Penalty Rule",
    description="Create a new attendance penalty rule.",
    request=AttendancePenaltyRulesSerializer,
    responses={
        201: get_api_response_serializer(AttendancePenaltyRulesSerializer, name="AttendancePenaltyRuleCreated"),
        400: get_api_response_serializer(name="ValidationError"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
def create(request):
    try:
        serializer = AttendancePenaltyRulesSerializer(data=request.data)
        if not serializer.is_valid():
            return ApiResponse(status.HTTP_400_BAD_REQUEST, "Invalid input data", serializer.errors)
        
        validated_data = serializer.validated_data
        validated_data['createdBy'] = request.user_id
        
        result = attendance_penalty_rules_service.create(validated_data)
        return ApiResponse(status.HTTP_201_CREATED, "Attendance penalty rules created successfully", result)
    except Exception as e:
        logger.error(f"create view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e), {})


@extend_schema(
    summary="Update Attendance Penalty Rule",
    description="Update an existing attendance penalty rule details by its ID.",
    parameters=[
        OpenApiParameter(name="id", description="Rule ID", required=True, type=int, location=OpenApiParameter.PATH)
    ],
    request=AttendancePenaltyRulesSerializer,
    responses={
        200: get_api_response_serializer(AttendancePenaltyRulesSerializer, name="AttendancePenaltyRuleUpdated"),
        400: get_api_response_serializer(name="ValidationError"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['PATCH', 'PUT'])
@authentication_classes([JWTAuthentication])
def update(request, id):
    try:
        rule_id = int(id)
        serializer = AttendancePenaltyRulesSerializer(data=request.data, partial=True)
        if not serializer.is_valid():
            return ApiResponse(status.HTTP_400_BAD_REQUEST, "Invalid input data", serializer.errors)
        
        validated_data = serializer.validated_data
        validated_data['createdBy'] = request.user_id
        
        result = attendance_penalty_rules_service.update(rule_id, validated_data)
        return ApiResponse(status.HTTP_200_OK, "Attendance penalty rules update successfully", result)
    except Exception as e:
        logger.error(f"update view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e), {})


@extend_schema(
    summary="Delete Attendance Penalty Rule",
    description="Delete an attendance penalty rule by its ID.",
    parameters=[
        OpenApiParameter(name="id", description="Rule ID", required=True, type=int, location=OpenApiParameter.PATH)
    ],
    responses={
        200: get_api_response_serializer(name="AttendancePenaltyRuleDeleted"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
def delete(request, id):
    try:
        rule_id = int(id)
        attendance_penalty_rules_service.delete_by_id(rule_id)
        return ApiResponse(status.HTTP_200_OK, "Attendance penalty rule deleted successfully", "")
    except Exception as e:
        logger.error(f"delete view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Fail to delete attendance penalty rule", {})

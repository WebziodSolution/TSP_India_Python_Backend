import logging
from rest_framework.decorators import api_view, authentication_classes
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter
from common.response.api_response import ApiResponse
from common.auth.authentication import JWTAuthentication
from common.exception.exception_handler import custom_exception_handler
from common.serializers import OvertimeRulesSerializer
from common.swagger_utils import get_api_response_serializer
from .service import OvertimeRulesService

logger = logging.getLogger(__name__)
exception_handler = custom_exception_handler

overtime_rules_service = OvertimeRulesService()

@extend_schema(
    summary="Get All Overtime Rules",
    description="Retrieve all overtime rules associated with a specific company.",
    parameters=[
        OpenApiParameter(name="id", description="Company ID", required=True, type=int, location=OpenApiParameter.PATH)
    ],
    responses={
        200: get_api_response_serializer(OvertimeRulesSerializer, many=True, name="CompanyOvertimeRulesList"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def get_all_overtime_rules(request, id):
    try:
        company_id = int(id)
        result = overtime_rules_service.get_all_overtime_rules(company_id)
        return ApiResponse(status.HTTP_200_OK, "Fetch overtime rules successfully", result)
    except Exception as e:
        logger.error(f"get_all_overtime_rules view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Fail to fetch overtime rules", {})


@extend_schema(
    summary="Get Overtime Rule By ID",
    description="Retrieve a single overtime rule by its ID.",
    parameters=[
        OpenApiParameter(name="id", description="Overtime Rule ID", required=True, type=int, location=OpenApiParameter.PATH)
    ],
    responses={
        200: get_api_response_serializer(OvertimeRulesSerializer, name="OvertimeRuleDetailsResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def get_overtime_rule(request, id):
    try:
        rule_id = int(id)
        result = overtime_rules_service.get_overtime_rule(rule_id)
        return ApiResponse(status.HTTP_200_OK, "Fetch overtime rules successfully", result)
    except Exception as e:
        logger.error(f"get_overtime_rule view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Fail to fetch overtime rules", {})


@extend_schema(
    summary="Create Overtime Rule",
    description="Create a new overtime rule for a company.",
    parameters=[
        OpenApiParameter(name="id", description="Company ID", required=True, type=int, location=OpenApiParameter.PATH)
    ],
    request=OvertimeRulesSerializer,
    responses={
        201: get_api_response_serializer(OvertimeRulesSerializer, name="OvertimeRuleCreatedResponse"),
        400: get_api_response_serializer(name="ValidationError"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
def create_overtime_rule(request, id):
    try:
        company_id = int(id)
        serializer = OvertimeRulesSerializer(data=request.data)
        if not serializer.is_valid():
            return ApiResponse(status.HTTP_400_BAD_REQUEST, "Invalid input data", serializer.errors)
        
        result = overtime_rules_service.create_overtime_rule(serializer.validated_data, company_id)
        return ApiResponse(status.HTTP_201_CREATED, "Overtime rule created successfully", result)
    except Exception as e:
        logger.error(f"create_overtime_rule view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e), {})


@extend_schema(
    summary="Update Overtime Rule",
    description="Update an existing overtime rule's details.",
    parameters=[
        OpenApiParameter(name="id", description="Overtime Rule ID", required=True, type=int, location=OpenApiParameter.PATH)
    ],
    request=OvertimeRulesSerializer,
    responses={
        200: get_api_response_serializer(OvertimeRulesSerializer, name="OvertimeRuleUpdatedResponse"),
        400: get_api_response_serializer(name="ValidationError"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['PATCH', 'PUT'])
@authentication_classes([JWTAuthentication])
def update_overtime_rule(request, id):
    try:
        rule_id = int(id)
        serializer = OvertimeRulesSerializer(data=request.data, partial=True)
        if not serializer.is_valid():
            return ApiResponse(status.HTTP_400_BAD_REQUEST, "Invalid input data", serializer.errors)
            
        result = overtime_rules_service.update_overtime_rule(rule_id, serializer.validated_data)
        return ApiResponse(status.HTTP_200_OK, "Overtime rule updated successfully", result)
    except Exception as e:
        logger.error(f"update_overtime_rule view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e), {})


@extend_schema(
    summary="Delete Overtime Rule",
    description="Delete an overtime rule by its ID.",
    parameters=[
        OpenApiParameter(name="id", description="Overtime Rule ID", required=True, type=int, location=OpenApiParameter.PATH)
    ],
    responses={
        200: get_api_response_serializer(name="OvertimeRuleDeletedResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
def delete_overtime_rule(request, id):
    try:
        rule_id = int(id)
        overtime_rules_service.delete_overtime_rule(rule_id)
        return ApiResponse(status.HTTP_200_OK, "Overtime rule deleted successfully", "")
    except Exception as e:
        logger.error(f"delete_overtime_rule view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e), {})

import logging
from rest_framework.decorators import api_view, authentication_classes
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter
from common.response.api_response import ApiResponse
from common.auth.authentication import JWTAuthentication
from common.serializers import DeductionsSerializer
from common.swagger_utils import get_api_response_serializer
from .service import DeductionsService

logger = logging.getLogger(__name__)
deductions_service = DeductionsService()

@extend_schema(
    summary="Get All Deductions for Employee",
    description="Retrieve list of all deductions details for a given employee ID.",
    parameters=[
        OpenApiParameter(name="id", description="Employee ID", required=True, type=int)
    ],
    responses={
        200: get_api_response_serializer(DeductionsSerializer, many=True, name="DeductionsListResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def get_all_deductions(request):
    try:
        emp_id = request.query_params.get("id")
        if emp_id is None:
            return ApiResponse(status.HTTP_400_BAD_REQUEST, "Employee ID parameter 'id' is required.", {})
        result = deductions_service.find_by_employee_id(int(emp_id))
        return ApiResponse(status.HTTP_200_OK, "Fetch deductions details successfully", result)
    except Exception as e:
        logger.error(f"get_all_deductions view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Fail to fetch deductions details", {})


@extend_schema(
    summary="Get Deduction by ID",
    description="Retrieve details of a deduction by ID.",
    parameters=[
        OpenApiParameter(name="id", description="Deduction ID", required=True, type=int, location=OpenApiParameter.PATH)
    ],
    responses={
        200: get_api_response_serializer(DeductionsSerializer, name="DeductionResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def get_deductions(request, id):
    try:
        deduction_id = int(id)
        result = deductions_service.find_by_id(deduction_id)
        return ApiResponse(status.HTTP_200_OK, "Fetch deductions details successfully", result)
    except Exception as e:
        logger.error(f"get_deductions view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Fail to fetch deductions details", {})


@extend_schema(
    summary="Save Deductions List",
    description="Save (create or update) a list of deductions.",
    request=DeductionsSerializer(many=True),
    responses={
        200: get_api_response_serializer(name="DeductionsSavedResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
def save_deductions(request):
    try:
        deductions_service.save_deductions(request.data)
        return ApiResponse(status.HTTP_200_OK, "Deductions save successfully", "")
    except Exception as e:
        logger.error(f"save_deductions view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Fail to save deductions", {})


@extend_schema(
    summary="Delete Deduction",
    description="Delete an existing deduction by ID.",
    parameters=[
        OpenApiParameter(name="id", description="Deduction ID", required=True, type=int, location=OpenApiParameter.PATH)
    ],
    responses={
        200: get_api_response_serializer(name="DeductionDeletedResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
def delete_deductions(request, id):
    try:
        deduction_id = int(id)
        deductions_service.delete_by_id(deduction_id)
        return ApiResponse(status.HTTP_200_OK, "Deductions delete successfully", "")
    except Exception as e:
        logger.error(f"delete_deductions view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Fail to delete deductions", {})

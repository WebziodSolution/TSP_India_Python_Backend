import logging
from rest_framework.decorators import api_view, authentication_classes
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter
from common.response.api_response import ApiResponse
from common.auth.authentication import JWTAuthentication
from common.exception.exception_handler import custom_exception_handler
from common.serializers import UserShiftSerializer
from common.swagger_utils import get_api_response_serializer
from .service import UserShiftService

logger = logging.getLogger(__name__)
exception_handler = custom_exception_handler

user_shift_service = UserShiftService()

@extend_schema(
    summary="Get All User Shifts",
    description="Retrieve all user shifts.",
    responses={
        200: get_api_response_serializer(UserShiftSerializer, many=True, name="UserShiftsList"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def get_all_shift(request):
    try:
        result = user_shift_service.getAllUserShift()
        return ApiResponse(status.HTTP_200_OK, "Shift fetched successfully", result)
    except Exception as e:
        logger.error(f"get_all_shift view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e), {})


@extend_schema(
    summary="Get User Shift By ID",
    description="Retrieve specific user shift by its ID.",
    parameters=[
        OpenApiParameter(name="id", description="User Shift ID", required=True, type=int, location=OpenApiParameter.PATH)
    ],
    responses={
        200: get_api_response_serializer(UserShiftSerializer, name="UserShiftResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def get_user_shift(request, id):
    try:
        shift_id = int(id)
        result = user_shift_service.getUserShift(shift_id)
        return ApiResponse(status.HTTP_200_OK, "Shift fetched successfully", result)
    except Exception as e:
        logger.error(f"get_user_shift view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e), {})


@extend_schema(
    summary="Create User Shift",
    description="Create a new user shift.",
    request=UserShiftSerializer,
    responses={
        201: get_api_response_serializer(UserShiftSerializer, name="UserShiftCreatedResponse"),
        400: get_api_response_serializer(name="ValidationError"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
def create_user_shift(request):
    try:
        serializer = UserShiftSerializer(data=request.data)
        if not serializer.is_valid():
            return ApiResponse(status.HTTP_400_BAD_REQUEST, "Invalid input data", serializer.errors)
        
        result = user_shift_service.createUserShift(serializer.validated_data)
        return ApiResponse(status.HTTP_201_CREATED, "Shift added successfully", "")
    except Exception as e:
        logger.error(f"create_user_shift view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e), {})


@extend_schema(
    summary="Update User Shift",
    description="Update an existing user shift's details.",
    parameters=[
        OpenApiParameter(name="id", description="User Shift ID", required=True, type=int, location=OpenApiParameter.PATH)
    ],
    request=UserShiftSerializer,
    responses={
        200: get_api_response_serializer(UserShiftSerializer, name="UserShiftUpdatedResponse"),
        400: get_api_response_serializer(name="ValidationError"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
def update_user_shift(request, id):
    try:
        shift_id = int(id)
        serializer = UserShiftSerializer(data=request.data)
        if not serializer.is_valid():
            return ApiResponse(status.HTTP_400_BAD_REQUEST, "Invalid input data", serializer.errors)
            
        result = user_shift_service.update_user_shift(shift_id, serializer.validated_data)
        return ApiResponse(status.HTTP_200_OK, "Shift updated successfully", "")
    except Exception as e:
        logger.error(f"update_user_shift view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e), {})


@extend_schema(
    summary="Delete User Shift",
    description="Delete a user shift by its ID.",
    parameters=[
        OpenApiParameter(name="id", description="User Shift ID", required=True, type=int, location=OpenApiParameter.PATH)
    ],
    responses={
        200: get_api_response_serializer(name="UserShiftDeletedResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
def delete_user_shift(request, id):
    try:
        shift_id = int(id)
        user_shift_service.deleteUserShift(shift_id)
        return ApiResponse(status.HTTP_200_OK, "Shift deleted successfully", "")
    except Exception as e:
        logger.error(f"delete_user_shift view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e), {})

import logging
from rest_framework.decorators import api_view, authentication_classes
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter
from common.response.api_response import ApiResponse
from common.auth.authentication import JWTAuthentication
from common.exception.exception_handler import custom_exception_handler
from common.serializers import FunctionalitySerializer
from common.swagger_utils import get_api_response_serializer
from .service import FunctionalityService

logger = logging.getLogger(__name__)
exception_handler = custom_exception_handler

functionality_service = FunctionalityService()

@extend_schema(
    summary="Get All Functionalities",
    description="Retrieve all functionalities.",
    responses={
        200: get_api_response_serializer(FunctionalitySerializer, many=True, name="FunctionalityListResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def get_all_functionality(request):
    try:
        result = functionality_service.getAllFunctionality()
        return ApiResponse(status.HTTP_200_OK, "Functionality fetched successfully", result)
    except Exception as e:
        logger.error(f"get_all_functionality view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e), {})


@extend_schema(
    summary="Get Functionality By ID",
    description="Retrieve a single functionality by ID.",
    parameters=[
        OpenApiParameter(name="id", description="Functionality ID", required=True, type=int, location=OpenApiParameter.PATH)
    ],
    responses={
        200: get_api_response_serializer(FunctionalitySerializer, name="FunctionalityDetailsResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def get_functionality(request, id):
    try:
        f_id = int(id)
        result = functionality_service.getFunctionality(f_id)
        return ApiResponse(status.HTTP_200_OK, "Functionality fetched successfully", result)
    except Exception as e:
        logger.error(f"get_functionality view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e), {})


@extend_schema(
    summary="Create Functionality",
    description="Create a new functionality.",
    request=FunctionalitySerializer,
    responses={
        201: get_api_response_serializer(FunctionalitySerializer, name="FunctionalityCreatedResponse"),
        400: get_api_response_serializer(name="ValidationError"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
def create_functionality(request):
    try:
        serializer = FunctionalitySerializer(data=request.data)
        if not serializer.is_valid():
            return ApiResponse(status.HTTP_400_BAD_REQUEST, "Invalid input data", serializer.errors)
        
        result = functionality_service.createFunctionality(serializer.validated_data)
        return ApiResponse(status.HTTP_201_CREATED, "Functionality created successfully", "")
    except Exception as e:
        logger.error(f"create_functionality view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e), {})


@extend_schema(
    summary="Update Functionality",
    description="Update an existing functionality.",
    parameters=[
        OpenApiParameter(name="id", description="Functionality ID", required=True, type=int, location=OpenApiParameter.PATH)
    ],
    request=FunctionalitySerializer,
    responses={
        200: get_api_response_serializer(FunctionalitySerializer, name="FunctionalityUpdatedResponse"),
        400: get_api_response_serializer(name="ValidationError"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
def update_functionality(request, id):
    try:
        f_id = int(id)
        serializer = FunctionalitySerializer(data=request.data)
        if not serializer.is_valid():
            return ApiResponse(status.HTTP_400_BAD_REQUEST, "Invalid input data", serializer.errors)
            
        result = functionality_service.updateFunctionality(f_id, serializer.validated_data)
        return ApiResponse(status.HTTP_200_OK, "Functionality update successfully", "")
    except Exception as e:
        logger.error(f"update_functionality view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e), {})


@extend_schema(
    summary="Delete Functionality",
    description="Delete a functionality by ID.",
    parameters=[
        OpenApiParameter(name="id", description="Functionality ID", required=True, type=int, location=OpenApiParameter.PATH)
    ],
    responses={
        200: get_api_response_serializer(name="FunctionalityDeletedResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
def delete_functionality(request, id):
    try:
        f_id = int(id)
        functionality_service.deleteFunctionality(f_id)
        return ApiResponse(status.HTTP_200_OK, "Functionality deleted successfully", "")
    except Exception as e:
        logger.error(f"delete_functionality view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e), {})

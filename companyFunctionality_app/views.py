import logging
from rest_framework.decorators import api_view, authentication_classes
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter
from common.response.api_response import ApiResponse
from common.auth.authentication import JWTAuthentication
from common.serializers import CompanyFunctionalitySerializer
from common.swagger_utils import get_api_response_serializer
from .service import CompanyFunctionalityService

logger = logging.getLogger(__name__)
functionality_service = CompanyFunctionalityService()

@extend_schema(
    summary="Get All Functionalities",
    description="Retrieve a list of all functionalities.",
    responses={
        200: get_api_response_serializer(CompanyFunctionalitySerializer, many=True, name="FunctionalityList"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def get_all_functionality(request):
    try:
        result = functionality_service.get_all_functionality()
        return ApiResponse(status.HTTP_200_OK, "Functionality fetched successfully", result)
    except Exception as e:
        logger.error(f"get_all_functionality view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e), {})


@extend_schema(
    summary="Get Functionality by ID",
    description="Retrieve details of a functionality by ID.",
    parameters=[
        OpenApiParameter(name="id", description="Functionality ID", required=True, type=int, location=OpenApiParameter.PATH)
    ],
    responses={
        200: get_api_response_serializer(CompanyFunctionalitySerializer, name="FunctionalityResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def get_functionality(request, id):
    try:
        func_id = int(id)
        result = functionality_service.get_functionality(func_id)
        return ApiResponse(status.HTTP_200_OK, "Functionality fetched successfully", result)
    except Exception as e:
        logger.error(f"get_functionality view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e), {})


@extend_schema(
    summary="Create Functionality",
    description="Create a new functionality.",
    request=CompanyFunctionalitySerializer,
    responses={
        201: get_api_response_serializer(CompanyFunctionalitySerializer, name="FunctionalityCreatedResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
def create_functionality(request):
    try:
        result = functionality_service.create_functionality(request.data)
        return ApiResponse(status.HTTP_201_CREATED, "Functionality created successfully", "")
    except Exception as e:
        logger.error(f"create_functionality view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e), {})


@extend_schema(
    summary="Update Functionality",
    description="Update an existing functionality by ID.",
    parameters=[
        OpenApiParameter(name="id", description="Functionality ID", required=True, type=int, location=OpenApiParameter.PATH)
    ],
    request=CompanyFunctionalitySerializer,
    responses={
        200: get_api_response_serializer(CompanyFunctionalitySerializer, name="FunctionalityUpdatedResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
def update_functionality(request, id):
    try:
        func_id = int(id)
        result = functionality_service.update_functionality(func_id, request.data)
        return ApiResponse(status.HTTP_200_OK, "Functionality update successfully", "")
    except Exception as e:
        logger.error(f"update_functionality view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e), {})


@extend_schema(
    summary="Delete Functionality",
    description="Delete an existing functionality by ID.",
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
        func_id = int(id)
        functionality_service.delete_functionality(func_id)
        return ApiResponse(status.HTTP_200_OK, "Functionality deleted successfully", "")
    except Exception as e:
        logger.error(f"delete_functionality view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e), {})

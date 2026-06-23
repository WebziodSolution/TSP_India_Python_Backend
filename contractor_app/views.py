import logging
from rest_framework.decorators import api_view, authentication_classes
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter
from common.response.api_response import ApiResponse
from common.auth.authentication import JWTAuthentication
from common.serializers import ContractorSerializer
from common.swagger_utils import get_api_response_serializer
from .service import ContractorService

logger = logging.getLogger(__name__)
contractor_service = ContractorService()

@extend_schema(
    summary="Get All Contractors",
    description="Retrieve list of all contractor details.",
    responses={
        200: get_api_response_serializer(ContractorSerializer, many=True, name="ContractorsListResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def get_all_contractors(request):
    try:
        result = contractor_service.get_all_contractors()
        return ApiResponse(status.HTTP_200_OK, "Fetch contractor details successfully", result)
    except Exception as e:
        logger.error(f"get_all_contractors view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Fail to fetch contractor details", {})


@extend_schema(
    summary="Get Contractor by ID",
    description="Retrieve details of a contractor by contractor ID.",
    parameters=[
        OpenApiParameter(name="id", description="Contractor ID", required=True, type=int, location=OpenApiParameter.PATH)
    ],
    responses={
        200: get_api_response_serializer(ContractorSerializer, name="ContractorResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def get_contractor(request, id):
    try:
        contractor_id = int(id)
        result = contractor_service.get_contractor(contractor_id)
        return ApiResponse(status.HTTP_200_OK, "Fetch contractor details successfully", result)
    except Exception as e:
        logger.error(f"get_contractor view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Fail to fetch contractor details", {})


@extend_schema(
    summary="Create Contractor",
    description="Create a new contractor details.",
    request=ContractorSerializer,
    responses={
        201: get_api_response_serializer(name="ContractorCreatedResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
def create_contractor(request):
    try:
        contractor_service.create_contractor(request.data)
        return ApiResponse(status.HTTP_201_CREATED, "Contractor details added successfully", "")
    except Exception as e:
        logger.error(f"create_contractor view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Fail to create contractor details", {})


@extend_schema(
    summary="Update Contractor",
    description="Update an existing contractor details by contractor ID.",
    parameters=[
        OpenApiParameter(name="id", description="Contractor ID", required=True, type=int, location=OpenApiParameter.PATH)
    ],
    request=ContractorSerializer,
    responses={
        200: get_api_response_serializer(name="ContractorUpdatedResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
def update_contractor(request, id):
    try:
        contractor_id = int(id)
        contractor_service.update_contractor(contractor_id, request.data)
        return ApiResponse(status.HTTP_200_OK, "Contractor details updated successfully", "")
    except Exception as e:
        logger.error(f"update_contractor view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Fail to update contractor details", {})


@extend_schema(
    summary="Delete Contractor",
    description="Delete an existing contractor by ID.",
    parameters=[
        OpenApiParameter(name="id", description="Contractor ID", required=True, type=int, location=OpenApiParameter.PATH)
    ],
    responses={
        200: get_api_response_serializer(name="ContractorDeletedResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
def delete_contractor(request, id):
    try:
        contractor_id = int(id)
        contractor_service.delete_contractor(contractor_id)
        return ApiResponse(status.HTTP_200_OK, "Contractor deleted successfully", "")
    except Exception as e:
        logger.error(f"delete_contractor view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Fail to delete contractor details", {})

import logging
from rest_framework.decorators import api_view, authentication_classes
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter
from common.response.api_response import ApiResponse
from common.auth.authentication import JWTAuthentication
from common.exception.exception_handler import custom_exception_handler
from common.serializers import LocationSerializer
from common.swagger_utils import get_api_response_serializer
from .service import LocationService

logger = logging.getLogger(__name__)
exception_handler = custom_exception_handler

location_service = LocationService()

@extend_schema(
    summary="Get Company Active Locations",
    description="Retrieve all active locations for a specific company.",
    parameters=[
        OpenApiParameter(name="id", description="Company ID", required=True, type=int, location=OpenApiParameter.PATH)
    ],
    responses={
        200: get_api_response_serializer(LocationSerializer, many=True, name="CompanyActiveLocationsList"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def get_company_active_locations(request, id):
    try:
        company_id = int(id)
        result = location_service.get_company_active_locations(company_id)
        return ApiResponse(status.HTTP_200_OK, "Fetch locations details successfully", result)
    except Exception as e:
        logger.error(f"get_company_active_locations view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Fail to fetch locations details", {})


@extend_schema(
    summary="Get All Locations By Company",
    description="Retrieve all locations (active or inactive) for a specific company.",
    parameters=[
        OpenApiParameter(name="id", description="Company ID", required=True, type=int, location=OpenApiParameter.PATH)
    ],
    responses={
        200: get_api_response_serializer(LocationSerializer, many=True, name="CompanyAllLocationsList"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def get_all_location_by_company(request, id):
    try:
        company_id = int(id)
        result = location_service.get_all_location_by_company(company_id)
        return ApiResponse(status.HTTP_200_OK, "Fetch locations details successfully", result)
    except Exception as e:
        logger.error(f"get_all_location_by_company view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Fail to fetch locations details", {})


@extend_schema(
    summary="Get All Locations",
    description="Retrieve all locations in the system.",
    responses={
        200: get_api_response_serializer(LocationSerializer, many=True, name="AllLocationsList"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def get_all_location(request):
    try:
        result = location_service.get_all_location()
        return ApiResponse(status.HTTP_200_OK, "Fetch locations details successfully", result)
    except Exception as e:
        logger.error(f"get_all_location view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Fail to fetch locations details", {})


@extend_schema(
    summary="Get Locations by IDs",
    description="Retrieve location details for a list of location IDs passed in query parameters.",
    parameters=[
        OpenApiParameter(name="locationIds", description="List of location IDs", required=True, type=int, many=True, location=OpenApiParameter.QUERY)
    ],
    responses={
        200: get_api_response_serializer(LocationSerializer, many=True, name="LocationsListByIds"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def get_locations(request):
    try:
        location_ids_str = request.query_params.getlist("locationIds")
        # Support both comma-separated and repeated parameters
        location_ids = []
        for val in location_ids_str:
            if "," in val:
                location_ids.extend([int(x.strip()) for x in val.split(",") if x.strip()])
            else:
                location_ids.append(int(val))
        
        result = location_service.get_locations(location_ids)
        return ApiResponse(status.HTTP_200_OK, "Fetched location details successfully", result)
    except Exception as e:
        logger.error(f"get_locations view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to fetch location details", {})


@extend_schema(
    summary="Get Location By ID",
    description="Retrieve specific location details by its ID.",
    parameters=[
        OpenApiParameter(name="id", description="Location ID", required=True, type=int, location=OpenApiParameter.PATH)
    ],
    responses={
        200: get_api_response_serializer(LocationSerializer, name="LocationDetailsResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def get_location(request, id):
    try:
        location_id = int(id)
        result = location_service.get_location(location_id)
        return ApiResponse(status.HTTP_200_OK, "Fetch locations details successfully", result)
    except Exception as e:
        logger.error(f"get_location view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Fail to fetch locations details", {})


@extend_schema(
    summary="Create Location",
    description="Create a new location.",
    request=LocationSerializer,
    responses={
        201: get_api_response_serializer(LocationSerializer, name="LocationCreatedResponse"),
        400: get_api_response_serializer(name="ValidationError"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
def create_location(request):
    try:
        serializer = LocationSerializer(data=request.data)
        if not serializer.is_valid():
            return ApiResponse(status.HTTP_400_BAD_REQUEST, "Invalid input data", serializer.errors)
        
        result = location_service.create_location(serializer.validated_data)
        return ApiResponse(status.HTTP_201_CREATED, "Locations details added successfully", "")
    except Exception as e:
        logger.error(f"create_location view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Fail to add locations details", {})


@extend_schema(
    summary="Update Location",
    description="Update an existing location's details.",
    parameters=[
        OpenApiParameter(name="id", description="Location ID", required=True, type=int, location=OpenApiParameter.PATH)
    ],
    request=LocationSerializer,
    responses={
        200: get_api_response_serializer(LocationSerializer, name="LocationUpdatedResponse"),
        400: get_api_response_serializer(name="ValidationError"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['PATCH', 'PUT'])
@authentication_classes([JWTAuthentication])
def update_location(request, id):
    try:
        location_id = int(id)
        serializer = LocationSerializer(data=request.data, partial=True)
        if not serializer.is_valid():
            return ApiResponse(status.HTTP_400_BAD_REQUEST, "Invalid input data", serializer.errors)
            
        result = location_service.update_location(location_id, serializer.validated_data)
        return ApiResponse(status.HTTP_200_OK, "Locations details updated successfully", "")
    except Exception as e:
        logger.error(f"update_location view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Fail to updated locations details", {})


@extend_schema(
    summary="Delete Location",
    description="Delete a location by its ID.",
    parameters=[
        OpenApiParameter(name="id", description="Location ID", required=True, type=int, location=OpenApiParameter.PATH)
    ],
    responses={
        200: get_api_response_serializer(name="LocationDeletedResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
def delete_location(request, id):
    try:
        location_id = int(id)
        location_service.delete_location(location_id)
        return ApiResponse(status.HTTP_200_OK, "Locations details deleted successfully", "")
    except Exception as e:
        logger.error(f"delete_location view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Fail to delete locations details", {})

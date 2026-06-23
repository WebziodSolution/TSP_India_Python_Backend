import logging
from rest_framework.decorators import api_view, authentication_classes
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter
from common.response.api_response import ApiResponse
from common.auth.authentication import JWTAuthentication
from common.serializers import CountryToStateSerializer
from common.swagger_utils import get_api_response_serializer
from .service import CountryToStateService

logger = logging.getLogger(__name__)
state_service = CountryToStateService()

@extend_schema(
    summary="Get All States",
    description="Retrieve details of all country-to-state mappings.",
    responses={
        200: get_api_response_serializer(CountryToStateSerializer, many=True, name="StatesListResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def get_all_state(request):
    try:
        result = state_service.get_all_state()
        return ApiResponse(status.HTTP_200_OK, "Fetch state details successfully", result)
    except Exception as e:
        logger.error(f"get_all_state view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Fail to fetch state details", {})


@extend_schema(
    summary="Get All States by Country ID",
    description="Retrieve all states associated with a country ID.",
    parameters=[
        OpenApiParameter(name="id", description="Country ID", required=True, type=int, location=OpenApiParameter.PATH)
    ],
    responses={
        200: get_api_response_serializer(CountryToStateSerializer, many=True, name="StatesListByCountryResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def get_all_state_by_country(request, id):
    try:
        country_id = int(id)
        result = state_service.get_all_state_by_country(country_id)
        return ApiResponse(status.HTTP_200_OK, "Fetch state details successfully", result)
    except Exception as e:
        logger.error(f"get_all_state_by_country view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Fail to fetch state details", {})

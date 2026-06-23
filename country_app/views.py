import logging
from rest_framework.decorators import api_view, authentication_classes
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter
from common.response.api_response import ApiResponse
from common.auth.authentication import JWTAuthentication
from common.serializers import CountrySerializer
from common.swagger_utils import get_api_response_serializer
from .service import CountryService

logger = logging.getLogger(__name__)
country_service = CountryService()

@extend_schema(
    summary="Get All Countries",
    description="Retrieve details of all countries.",
    responses={
        200: get_api_response_serializer(CountrySerializer, many=True, name="CountriesListResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def get_all_country(request):
    try:
        result = country_service.get_all_country()
        return ApiResponse(status.HTTP_200_OK, "Fetch country details successfully", result)
    except Exception as e:
        logger.error(f"get_all_country view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Fail to fetch country details", {})


@extend_schema(
    summary="Get Country by ID",
    description="Retrieve details of a country by country ID.",
    parameters=[
        OpenApiParameter(name="id", description="Country ID", required=True, type=int, location=OpenApiParameter.PATH)
    ],
    responses={
        200: get_api_response_serializer(CountrySerializer, name="CountryResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def get_country(request, id):
    try:
        country_id = int(id)
        result = country_service.get_country(country_id)
        return ApiResponse(status.HTTP_200_OK, "Fetch country details successfully", result)
    except Exception as e:
        logger.error(f"get_country view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Fail to fetch country details", {})

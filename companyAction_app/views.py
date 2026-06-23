import logging
from rest_framework.decorators import api_view, authentication_classes
from rest_framework import status
from drf_spectacular.utils import extend_schema
from common.response.api_response import ApiResponse
from common.auth.authentication import JWTAuthentication
from common.serializers import CompanyActionsSerializer
from common.swagger_utils import get_api_response_serializer
from .service import CompanyActionService

logger = logging.getLogger(__name__)
action_service = CompanyActionService()

@extend_schema(
    summary="Get All Actions",
    description="Retrieve list of all company actions details.",
    responses={
        200: get_api_response_serializer(CompanyActionsSerializer, many=True, name="CompanyActionsList"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def get_all_actions(request):
    try:
        result = action_service.get_all_actions()
        return ApiResponse(status.HTTP_200_OK, "Fetch actions details successfully", result)
    except Exception as e:
        logger.error(f"getAllActions view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Fail to fetch actions details", {})

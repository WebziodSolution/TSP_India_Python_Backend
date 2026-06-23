import logging
from rest_framework.decorators import api_view, authentication_classes
from rest_framework import status
from drf_spectacular.utils import extend_schema
from common.response.api_response import ApiResponse
from common.auth.authentication import JWTAuthentication
from common.exception.exception_handler import custom_exception_handler
from common.serializers import ActionSerializer
from common.swagger_utils import get_api_response_serializer
from .service import ActionService

logger = logging.getLogger(__name__)
exception_handler = custom_exception_handler

action_service = ActionService()

@extend_schema(
    summary="Get All Actions",
    description="Retrieve list of all actions in the system.",
    responses={
        200: get_api_response_serializer(ActionSerializer, many=True, name="ActionsListResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def get_all_actions(request):
    try:
        result = action_service.getAllActions()
        return ApiResponse(status.HTTP_200_OK, "Fetch actions details successfully", result)
    except Exception as e:
        logger.error(f"get_all_actions view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Fail to fetch actions details", {})

import logging
from rest_framework.decorators import api_view, authentication_classes
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter
from common.response.api_response import ApiResponse
from common.auth.authentication import JWTAuthentication
from common.serializers import CompanyActionsSerializer
from common.swagger_utils import get_api_response_serializer
from .service import CompanyRoleActionService

logger = logging.getLogger(__name__)
company_role_action_service = CompanyRoleActionService()

@extend_schema(
    summary="Get All Company Role Actions",
    description="Retrieve a list of all company role actions.",
    responses={
        200: get_api_response_serializer(CompanyActionsSerializer, many=True, name="CompanyActionsList"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def get_all_company_role_actions(request):
    try:
        result = company_role_action_service.get_company_actions()
        return ApiResponse(status.HTTP_200_OK, "Fetch actions details successfully", result)
    except Exception as e:
        logger.error(f"get_all_company_role_actions view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Fail to fetch actions details", {})


@extend_schema(
    summary="Get Action by ID",
    description="Retrieve details of a company role action by ID.",
    parameters=[
        OpenApiParameter(name="id", description="Action ID", required=True, type=int, location=OpenApiParameter.PATH)
    ],
    responses={
        200: get_api_response_serializer(CompanyActionsSerializer, name="CompanyActionResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def get_action(request, id):
    try:
        action_id = int(id)
        result = company_role_action_service.get_actions(action_id)
        return ApiResponse(status.HTTP_200_OK, "Fetch actions details successfully", result)
    except Exception as e:
        logger.error(f"get_action view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Fail to fetch actions details", {})


@extend_schema(
    summary="Create Action",
    description="Create a new company role action.",
    request=CompanyActionsSerializer,
    responses={
        201: get_api_response_serializer(CompanyActionsSerializer, name="CompanyActionCreatedResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
def create_action(request):
    try:
        result = company_role_action_service.create_actions(request.data)
        return ApiResponse(status.HTTP_201_CREATED, "Actions created successfully", result)
    except Exception as e:
        logger.error(f"create_action view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Fail to create action", {})


@extend_schema(
    summary="Update Action",
    description="Update an existing company role action by ID.",
    parameters=[
        OpenApiParameter(name="id", description="Action ID", required=True, type=int, location=OpenApiParameter.PATH)
    ],
    request=CompanyActionsSerializer,
    responses={
        200: get_api_response_serializer(CompanyActionsSerializer, name="CompanyActionUpdatedResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
def update_action(request, id):
    try:
        action_id = int(id)
        result = company_role_action_service.update_actions(action_id, request.data)
        return ApiResponse(status.HTTP_200_OK, "Actions updated successfully", result)
    except Exception as e:
        logger.error(f"update_action view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Fail to update action", {})


@extend_schema(
    summary="Delete Action",
    description="Delete an existing company role action by ID.",
    parameters=[
        OpenApiParameter(name="id", description="Action ID", required=True, type=int, location=OpenApiParameter.PATH)
    ],
    responses={
        200: get_api_response_serializer(name="CompanyActionDeletedResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
def delete_action(request, id):
    try:
        action_id = int(id)
        company_role_action_service.delete_actions(action_id)
        return ApiResponse(status.HTTP_200_OK, "Actions deleted successfully", "")
    except Exception as e:
        logger.error(f"delete_action view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Fail to delete action", {})

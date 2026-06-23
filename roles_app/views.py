import logging
from rest_framework.decorators import api_view, authentication_classes
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter
from common.response.api_response import ApiResponse
from common.auth.authentication import JWTAuthentication
from common.exception.exception_handler import custom_exception_handler
from common.serializers import RoleSerializer
from common.swagger_utils import get_api_response_serializer
from .service import RoleService

logger = logging.getLogger(__name__)
exception_handler = custom_exception_handler

role_service = RoleService()

@extend_schema(
    summary="Get All Roles List",
    description="Retrieve simplified list of all roles in the system.",
    responses={
        200: get_api_response_serializer(RoleSerializer, many=True, name="RolesListResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def get_all_roles_list(request):
    try:
        result = role_service.getAllRolesList()
        return ApiResponse(status.HTTP_200_OK, "Roles list fetched successfully", result)
    except Exception as e:
        logger.error(f"get_all_roles_list view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to fetch roles list", {})


@extend_schema(
    summary="Create Role",
    description="Add a new role and assign its policies.",
    request=RoleSerializer,
    responses={
        201: get_api_response_serializer(name="RoleCreatedResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
def create_role(request):
    try:
        result = role_service.createRole(request.data)
        return ApiResponse(status.HTTP_201_CREATED, "Role added successfully", {"role": result})
    except Exception as e:
        logger.error(f"create_role view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "failed to add new role", {})


@extend_schema(
    summary="Get Roles List Page",
    description="Retrieve paginated list of roles with policies.",
    parameters=[
        OpenApiParameter(name="searchKey", description="Search term", required=False, type=str),
        OpenApiParameter(name="page", description="Page index (0-indexed)", required=False, type=int),
        OpenApiParameter(name="size", description="Page size", required=False, type=int)
    ],
    responses={
        200: get_api_response_serializer(name="RolesListPageResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def roles_list(request):
    try:
        search_key = request.query_params.get("searchKey", "")
        page_str = request.query_params.get("page")
        size_str = request.query_params.get("size")
        
        page = int(page_str) if page_str else 0
        size = int(size_str) if size_str else 10
        
        result = role_service.rolesList(search_key, page, size)
        return ApiResponse(status.HTTP_200_OK, "Roles list fetched successfully", result)
    except Exception as e:
        logger.error(f"roles_list view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to fetch roles list", {})


@extend_schema(
    summary="Get All Roles Except Owner",
    description="Retrieve all roles except Owner.",
    responses={
        200: get_api_response_serializer(name="AllRolesListResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def get_all_roles(request):
    try:
        result = role_service.getAllRoles()
        return ApiResponse(status.HTTP_200_OK, "Roles list fetched successfully", result)
    except Exception as e:
        logger.error(f"get_all_roles view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to fetch roles list", {})


@extend_schema(
    summary="Get Role by ID",
    description="Retrieve details of a single role by ID.",
    parameters=[
        OpenApiParameter(name="roleId", description="Role ID", required=True, type=int, location=OpenApiParameter.PATH)
    ],
    responses={
        200: get_api_response_serializer(RoleSerializer, name="RoleResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def get_role_by_id(request, roleId):
    try:
        role_id = int(roleId)
        result = role_service.getRoleById(role_id)
        return ApiResponse(status.HTTP_200_OK, "Role fetched successfully", {"role": result})
    except Exception as e:
        logger.error(f"get_role_by_id view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to fetch role", {})


@extend_schema(
    summary="Update Role by ID",
    description="Update a role and its policy permissions by ID.",
    parameters=[
        OpenApiParameter(name="roleId", description="Role ID", required=True, type=int, location=OpenApiParameter.PATH)
    ],
    request=RoleSerializer,
    responses={
        200: get_api_response_serializer(RoleSerializer, name="RoleUpdatedResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
def update_role_by_id(request, roleId):
    try:
        role_id = int(roleId)
        result = role_service.updateById(role_id, request.data)
        return ApiResponse(status.HTTP_200_OK, "Role updated successfully", {"role": result})
    except Exception as e:
        logger.error(f"update_role_by_id view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to update role", {})


@extend_schema(
    summary="Delete Role by ID",
    description="Delete an existing role by ID.",
    parameters=[
        OpenApiParameter(name="roleId", description="Role ID", required=True, type=int, location=OpenApiParameter.PATH)
    ],
    responses={
        200: get_api_response_serializer(name="RoleDeletedResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
def delete_role_by_id(request, roleId):
    try:
        role_id = int(roleId)
        role_service.deleteRoleById(role_id)
        return ApiResponse(status.HTTP_200_OK, "Role deleted successfully", {})
    except Exception as e:
        logger.error(f"delete_role_by_id view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to delete role", {})


@extend_schema(
    summary="Get Role Policies by ID",
    description="Retrieve the role's mapped policy actions.",
    parameters=[
        OpenApiParameter(name="roleId", description="Role ID", required=True, type=int, location=OpenApiParameter.PATH)
    ],
    responses={
        200: get_api_response_serializer(name="RolePoliciesResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def get_actions(request, roleId):
    try:
        role_id = int(roleId)
        result = role_service.getPolicy(role_id)
        return ApiResponse(status.HTTP_200_OK, "Role's policies fetched successfully", result)
    except Exception as e:
        logger.error(f"get_actions view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to fetch", {})

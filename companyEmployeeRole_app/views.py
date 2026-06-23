import logging
from rest_framework.decorators import api_view, authentication_classes
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter
from common.response.api_response import ApiResponse
from common.auth.authentication import JWTAuthentication
from common.serializers import (
    CompanyEmployeeRolesSerializer,
    CompanyEmployeeRolesActionsSerializer
)
from common.swagger_utils import get_api_response_serializer
from .service import CompanyEmployeeRoleService

logger = logging.getLogger(__name__)
role_service = CompanyEmployeeRoleService()

@extend_schema(
    summary="Get All Roles List",
    description="Retrieve a list of all company employee roles with names and IDs.",
    responses={
        200: get_api_response_serializer(CompanyEmployeeRolesSerializer, many=True, name="RolesListOnlyResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def get_all_roles_list(request):
    try:
        result = role_service.get_all_roles_list()
        return ApiResponse(status.HTTP_200_OK, "Roles list fetched successfully", result)
    except Exception as e:
        logger.error(f"get_all_roles_list view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to fetch roles list", {})


@extend_schema(
    summary="Roles List Page",
    description="Retrieve a paginated and search-filtered list of all roles.",
    parameters=[
        OpenApiParameter(name="searchKey", description="Search by role name", required=False, type=str),
        OpenApiParameter(name="page", description="Page index (0-based)", required=False, type=int),
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
        page = int(request.query_params.get("page", 0))
        size = int(request.query_params.get("size", 10))
        result = role_service.roles_list(search_key, page, size)
        return ApiResponse(status.HTTP_200_OK, "Roles list fetched successfully", result)
    except Exception as e:
        logger.error(f"roles_list view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to fetch roles list", {})


@extend_schema(
    summary="Get All Roles (Except Owner)",
    description="Retrieve a list of all roles except the Owner role.",
    responses={
        200: get_api_response_serializer(name="RolesListExceptOwnerResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def get_all_roles(request):
    try:
        result = role_service.get_all_roles()
        return ApiResponse(status.HTTP_200_OK, "Roles list fetched successfully", result)
    except Exception as e:
        logger.error(f"get_all_roles view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to fetch roles list", {})


@extend_schema(
    summary="Get Actions / Policies for Role",
    description="Retrieve the policies and action mappings for a given role ID.",
    parameters=[
        OpenApiParameter(name="roleId", description="Role ID", required=True, type=int, location=OpenApiParameter.PATH)
    ],
    responses={
        200: get_api_response_serializer(CompanyEmployeeRolesActionsSerializer, name="RoleActionsPolicyResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def get_actions(request, roleId):
    try:
        role_id = int(roleId)
        result = role_service.get_policy(role_id)
        return ApiResponse(status.HTTP_200_OK, "Role's policies fetched successfully", result)
    except Exception as e:
        logger.error(f"get_actions view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to fetch", {})


@extend_schema(
    summary="Get All Roles by Company ID",
    description="Retrieve all employee roles associated with a company ID.",
    parameters=[
        OpenApiParameter(name="id", description="Company ID", required=True, type=int, location=OpenApiParameter.PATH)
    ],
    responses={
        200: get_api_response_serializer(CompanyEmployeeRolesSerializer, many=True, name="RolesListByCompanyResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def get_all_company_employee_roles(request, id):
    try:
        company_id = int(id)
        result = role_service.get_all_roles_by_company_id(company_id)
        return ApiResponse(status.HTTP_200_OK, "Fetch employee roles successfully", result)
    except Exception as e:
        logger.error(f"get_all_company_employee_roles view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Fail to fetch employee roles", {})


@extend_schema(
    summary="Get Employee Role by ID",
    description="Retrieve employee role details and its policies by role ID.",
    parameters=[
        OpenApiParameter(name="id", description="Role ID", required=True, type=int, location=OpenApiParameter.PATH)
    ],
    responses={
        200: get_api_response_serializer(CompanyEmployeeRolesSerializer, name="CompanyEmployeeRoleResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def get_employee_roles(request, id):
    try:
        role_id = int(id)
        result = role_service.get_role(role_id)
        return ApiResponse(status.HTTP_200_OK, "Fetch employee roles successfully", result)
    except Exception as e:
        logger.error(f"get_employee_roles view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Fail to fetch employee roles", {})


@extend_schema(
    summary="Create Employee Role",
    description="Add a new employee role with policies assignment.",
    request=CompanyEmployeeRolesSerializer,
    responses={
        201: get_api_response_serializer(name="RoleCreatedResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
def create_employee_roles(request):
    try:
        role_service.create_role(request.data)
        return ApiResponse(status.HTTP_201_CREATED, "Employee role added successfully", "")
    except Exception as e:
        logger.error(f"create_employee_roles view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Fail to add employee roles", {})


@extend_schema(
    summary="Update Employee Role",
    description="Update details and policies of an existing employee role.",
    parameters=[
        OpenApiParameter(name="id", description="Role ID", required=True, type=int, location=OpenApiParameter.PATH)
    ],
    request=CompanyEmployeeRolesSerializer,
    responses={
        200: get_api_response_serializer(name="RoleUpdatedResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
def update_employee_roles(request, id):
    try:
        role_id = int(id)
        role_service.update_role(role_id, request.data)
        return ApiResponse(status.HTTP_200_OK, "Employee role updated successfully", "")
    except Exception as e:
        logger.error(f"update_employee_roles view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Fail to update employee roles", {})


@extend_schema(
    summary="Delete Employee Role",
    description="Delete an existing employee role by ID.",
    parameters=[
        OpenApiParameter(name="id", description="Role ID", required=True, type=int, location=OpenApiParameter.PATH)
    ],
    responses={
        200: get_api_response_serializer(name="RoleDeletedResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
def delete_employee_roles(request, id):
    try:
        role_id = int(id)
        role_service.delete_role(role_id)
        return ApiResponse(status.HTTP_200_OK, "Employee role deleted successfully", "")
    except Exception as e:
        logger.error(f"delete_employee_roles view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Fail to delete employee roles", {})

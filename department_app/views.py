import logging
from rest_framework.decorators import api_view, authentication_classes
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter
from common.response.api_response import ApiResponse
from common.auth.authentication import JWTAuthentication
from common.serializers import DepartmentSerializer
from common.swagger_utils import get_api_response_serializer
from .service import DepartmentService

logger = logging.getLogger(__name__)
department_service = DepartmentService()

@extend_schema(
    summary="Get All Departments",
    description="Retrieve details of all departments associated with a company ID.",
    parameters=[
        OpenApiParameter(name="companyId", description="Company ID", required=True, type=int, location=OpenApiParameter.PATH)
    ],
    responses={
        200: get_api_response_serializer(DepartmentSerializer, many=True, name="DepartmentsListResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def get_all_department(request, companyId):
    try:
        comp_id = int(companyId)
        result = department_service.get_all_departments(comp_id)
        return ApiResponse(status.HTTP_200_OK, "Fetch department details successfully", result)
    except Exception as e:
        logger.error(f"get_all_department view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Fail to fetch departments details", {})


@extend_schema(
    summary="Get Department by ID",
    description="Retrieve details of a department by ID.",
    parameters=[
        OpenApiParameter(name="id", description="Department ID", required=True, type=int, location=OpenApiParameter.PATH)
    ],
    responses={
        200: get_api_response_serializer(DepartmentSerializer, name="DepartmentResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def get_department(request, id):
    try:
        dept_id = int(id)
        result = department_service.get_department(dept_id)
        return ApiResponse(status.HTTP_200_OK, "Fetch department details successfully", result)
    except Exception as e:
        logger.error(f"get_department view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Fail to fetch department details", {})


@extend_schema(
    summary="Create Department",
    description="Create a new department.",
    request=DepartmentSerializer,
    responses={
        201: get_api_response_serializer(name="DepartmentCreatedResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
def create_department(request):
    try:
        department_service.create_department(request.data)
        return ApiResponse(status.HTTP_201_CREATED, "Create department details successfully", "")
    except Exception as e:
        logger.error(f"create_department view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Fail to create department details", {})


@extend_schema(
    summary="Update Department",
    description="Update an existing department by ID.",
    parameters=[
        OpenApiParameter(name="id", description="Department ID", required=True, type=int, location=OpenApiParameter.PATH)
    ],
    request=DepartmentSerializer,
    responses={
        200: get_api_response_serializer(name="DepartmentUpdatedResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
def update_department(request, id):
    try:
        dept_id = int(id)
        department_service.update_department(dept_id, request.data)
        return ApiResponse(status.HTTP_200_OK, "Update department details successfully", "")
    except Exception as e:
        logger.error(f"update_department view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Fail to update department details", {})


@extend_schema(
    summary="Delete Department",
    description="Delete an existing department by ID.",
    parameters=[
        OpenApiParameter(name="id", description="Department ID", required=True, type=int, location=OpenApiParameter.PATH)
    ],
    responses={
        200: get_api_response_serializer(name="DepartmentDeletedResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
def delete_department(request, id):
    try:
        dept_id = int(id)
        department_service.delete_department(dept_id)
        return ApiResponse(status.HTTP_200_OK, "Delete department details successfully", "")
    except Exception as e:
        logger.error(f"delete_department view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Fail to delete department details", {})

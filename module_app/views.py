import logging
from rest_framework.decorators import api_view, authentication_classes
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter
from common.response.api_response import ApiResponse
from common.auth.authentication import JWTAuthentication
from common.exception.exception_handler import custom_exception_handler
from common.serializers import ModuleSerializer
from common.swagger_utils import get_api_response_serializer
from .service import ModuleService

logger = logging.getLogger(__name__)
exception_handler = custom_exception_handler

module_service = ModuleService()

@extend_schema(
    summary="Create Module",
    description="Add a new module and assign policies.",
    request=ModuleSerializer,
    responses={
        200: get_api_response_serializer(name="ModuleCreatedResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
def create_module(request):
    try:
        result = module_service.createModule(request.data)
        return ApiResponse(status.HTTP_200_OK, "Module added successfully", {"module": result})
    except Exception as e:
        logger.error(f"create_module view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "failed to add new module", {})


@extend_schema(
    summary="Get All Modules List Page",
    description="Retrieve a paginated list of modules, with optional search filter.",
    parameters=[
        OpenApiParameter(name="searchKey", description="Search term for module name", required=False, type=str),
        OpenApiParameter(name="page", description="Page index (0-indexed)", required=False, type=int),
        OpenApiParameter(name="size", description="Page size", required=False, type=int)
    ],
    responses={
        200: get_api_response_serializer(name="ModulesListPageResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def all_module_list_page(request):
    try:
        search_key = request.query_params.get("searchKey", "")
        page_str = request.query_params.get("page")
        size_str = request.query_params.get("size")
        
        # Support default pageable values parsed by DRF spectacular/pageable if any
        # Spring's pageable defaults usually pass via 'page' and 'size'
        page = int(page_str) if page_str else 0
        size = int(size_str) if size_str else 10
        
        result = module_service.allModuleListPage(search_key, page, size)
        return ApiResponse(status.HTTP_200_OK, "Modules list fetched successfully", result)
    except Exception as e:
        logger.error(f"all_module_list_page view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to fetch modules list", {})


@extend_schema(
    summary="Get Modules by Functionality List Page",
    description="Retrieve a paginated list of modules matching a functionality ID.",
    parameters=[
        OpenApiParameter(name="functionalityId", description="Functionality ID", required=True, type=int),
        OpenApiParameter(name="searchKey", description="Search term for module name", required=False, type=str),
        OpenApiParameter(name="page", description="Page index (0-indexed)", required=False, type=int),
        OpenApiParameter(name="size", description="Page size", required=False, type=int)
    ],
    responses={
        200: get_api_response_serializer(name="ModulesByFuncListPageResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def module_by_functionality_list_page(request):
    try:
        func_id_str = request.query_params.get("functionalityId")
        if not func_id_str:
            return ApiResponse(status.HTTP_400_BAD_REQUEST, "Missing functionalityId parameter", {})
            
        functionality_id = int(func_id_str)
        search_key = request.query_params.get("searchKey", "")
        page_str = request.query_params.get("page")
        size_str = request.query_params.get("size")
        
        page = int(page_str) if page_str else 0
        size = int(size_str) if size_str else 10
        
        result = module_service.moduleByFunctionalityListPage(functionality_id, search_key, page, size)
        return ApiResponse(status.HTTP_200_OK, "Modules list fetched successfully", result)
    except Exception as e:
        logger.error(f"module_by_functionality_list_page view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to fetch modules list", {})


@extend_schema(
    summary="Get All Modules",
    description="Retrieve a list of all modules.",
    responses={
        200: get_api_response_serializer(name="AllModulesListResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def get_all_modules(request):
    try:
        result = module_service.getAllModules()
        return ApiResponse(status.HTTP_200_OK, "Modules list fetched successfully", result)
    except Exception as e:
        logger.error(f"get_all_modules view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to fetch modules list", {})


@extend_schema(
    summary="Get Module by ID",
    description="Retrieve details of a module by ID.",
    parameters=[
        OpenApiParameter(name="moduleId", description="Module ID", required=True, type=int, location=OpenApiParameter.PATH)
    ],
    responses={
        200: get_api_response_serializer(ModuleSerializer, name="ModuleResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def get_module_by_id(request, moduleId):
    try:
        module_id = int(moduleId)
        result = module_service.getModuleById(module_id)
        return ApiResponse(status.HTTP_200_OK, "Module fetched successfully", {"module": result})
    except Exception as e:
        logger.error(f"get_module_by_id view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to fetch functionality", {})


@extend_schema(
    summary="Update Module by ID",
    description="Update an existing module and its policies by ID.",
    parameters=[
        OpenApiParameter(name="moduleId", description="Module ID", required=True, type=int, location=OpenApiParameter.PATH)
    ],
    request=ModuleSerializer,
    responses={
        200: get_api_response_serializer(ModuleSerializer, name="ModuleUpdatedResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
def update_module_by_id(request, moduleId):
    try:
        module_id = int(moduleId)
        result = module_service.updateModuleById(module_id, request.data)
        return ApiResponse(status.HTTP_200_OK, "Module updated successfully", {"module": result})
    except Exception as e:
        logger.error(f"update_module_by_id view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to update Module", {})


@extend_schema(
    summary="Delete Module by ID",
    description="Delete an existing module by ID.",
    parameters=[
        OpenApiParameter(name="moduleId", description="Module ID", required=True, type=int, location=OpenApiParameter.PATH)
    ],
    responses={
        200: get_api_response_serializer(name="ModuleDeletedResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
def delete_module_by_id(request, moduleId):
    try:
        module_id = int(moduleId)
        module_service.deleteModuleById(module_id)
        return ApiResponse(status.HTTP_200_OK, "Module deleted successfully", {})
    except Exception as e:
        logger.error(f"delete_module_by_id view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to delete module", {})

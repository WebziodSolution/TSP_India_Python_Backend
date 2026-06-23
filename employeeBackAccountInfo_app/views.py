import logging
from rest_framework.decorators import api_view, authentication_classes
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter
from common.response.api_response import ApiResponse
from common.auth.authentication import JWTAuthentication
from common.serializers import EmployeeBackAccountInfoSerializer
from common.swagger_utils import get_api_response_serializer
from .service import EmployeeBankAccountInfoService

logger = logging.getLogger(__name__)
bank_service = EmployeeBankAccountInfoService()

@extend_schema(
    summary="Create Bank Account Info",
    description="Add a new bank account info details for an employee.",
    request=EmployeeBackAccountInfoSerializer,
    responses={
        201: get_api_response_serializer(EmployeeBackAccountInfoSerializer, name="BankAccountInfoCreatedResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
def create_bank_account_info(request):
    try:
        result = bank_service.create_bank_account_info(request.data)
        return ApiResponse(status.HTTP_201_CREATED, "Bank Account Info added successfully", result)
    except Exception as e:
        logger.error(f"create_bank_account_info view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to add bank account info", {})


@extend_schema(
    summary="Get Bank Account Info by ID",
    description="Retrieve employee bank account details by ID.",
    parameters=[
        OpenApiParameter(name="id", description="Bank Info ID", required=True, type=int, location=OpenApiParameter.PATH)
    ],
    responses={
        200: get_api_response_serializer(EmployeeBackAccountInfoSerializer, name="BankAccountInfoResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def get_bank_account_info_by_id(request, id):
    try:
        bank_id = int(id)
        result = bank_service.get_bank_account_info_by_id(bank_id)
        return ApiResponse(status.HTTP_200_OK, "Fetch Bank Account Info successfully", result)
    except Exception as e:
        logger.error(f"get_bank_account_info_by_id view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to fetch Bank Account Info", {})


@extend_schema(
    summary="Get All Bank Account Info",
    description="Retrieve a list of all bank account info details.",
    responses={
        200: get_api_response_serializer(EmployeeBackAccountInfoSerializer, many=True, name="BankAccountInfoListResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def get_all_bank_account_info(request):
    try:
        result = bank_service.get_all_bank_account_info()
        return ApiResponse(status.HTTP_200_OK, "Fetch all Bank Account Info successfully", result)
    except Exception as e:
        logger.error(f"get_all_bank_account_info view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to fetch Bank Account Info", {})


@extend_schema(
    summary="Update Bank Account Info",
    description="Update bank account info details by ID.",
    parameters=[
        OpenApiParameter(name="id", description="Bank Info ID", required=True, type=int, location=OpenApiParameter.PATH)
    ],
    request=EmployeeBackAccountInfoSerializer,
    responses={
        200: get_api_response_serializer(EmployeeBackAccountInfoSerializer, name="BankAccountInfoUpdatedResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
def update_bank_account_info(request, id):
    try:
        bank_id = int(id)
        result = bank_service.update_bank_account_info(bank_id, request.data)
        return ApiResponse(status.HTTP_200_OK, "Bank Account Info updated successfully", result)
    except Exception as e:
        logger.error(f"update_bank_account_info view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to update Bank Account Info", {})


@extend_schema(
    summary="Delete Bank Account Info",
    description="Delete bank account info details by ID.",
    parameters=[
        OpenApiParameter(name="id", description="Bank Info ID", required=True, type=int, location=OpenApiParameter.PATH)
    ],
    responses={
        200: get_api_response_serializer(name="BankAccountInfoDeletedResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
def delete_bank_account_info(request, id):
    try:
        bank_id = int(id)
        bank_service.delete_bank_account_info(bank_id)
        return ApiResponse(status.HTTP_200_OK, "Bank Account Info deleted successfully", {})
    except Exception as e:
        logger.error(f"delete_bank_account_info view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to delete Bank Account Info", {})


@extend_schema(
    summary="Upload Passbook Image",
    description="Upload/Update bank account passbook image.",
    request=get_api_response_serializer(name="UploadPassbookImageRequest"),
    responses={
        200: get_api_response_serializer(name="UploadPassbookImageResponse"),
        404: get_api_response_serializer(name="ErrorResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
def upload_passbook_image(request):
    try:
        company_id = int(request.data.get("companyId"))
        bank_id = int(request.data.get("bankId"))
        bank_image_path = request.data.get("bank")
        
        path = bank_service.upload_passbook_image(company_id, bank_id, bank_image_path)
        if path == "Error":
            return ApiResponse(status.HTTP_404_NOT_FOUND, "Image does not exist in the directory", "")
        return ApiResponse(status.HTTP_200_OK, "Passbook image update successfully", path)
    except Exception as e:
        logger.error(f"upload_passbook_image view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Fail to update passbook image", {})


@extend_schema(
    summary="Delete Passbook Image",
    description="Delete passbook image associated with a bank ID.",
    parameters=[
        OpenApiParameter(name="companyId", description="Company ID", required=True, type=int, location=OpenApiParameter.PATH),
        OpenApiParameter(name="bankId", description="Bank Info ID", required=True, type=int, location=OpenApiParameter.PATH)
    ],
    responses={
        200: get_api_response_serializer(name="DeletePassbookImageResponse"),
        500: get_api_response_serializer(name="ErrorResponse")
    }
)
@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
def delete_passbook_image(request, companyId, bankId):
    try:
        comp_id = int(companyId)
        b_id = int(bankId)
        if bank_service.delete_passbook_image(comp_id, b_id):
            return ApiResponse(status.HTTP_200_OK, "Passbook image deleted successfully", "")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Passbook image not found", "")
    except Exception as e:
        logger.error(f"delete_passbook_image view error: {e}")
        return ApiResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, "Fail to delete passbook image", {})

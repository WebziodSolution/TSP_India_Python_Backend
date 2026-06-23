from rest_framework.views import exception_handler
from rest_framework.exceptions import ValidationError, AuthenticationFailed, NotAuthenticated, PermissionDenied
from rest_framework.response import Response
from rest_framework import status
from common.response.api_response import ApiResponse
from .exceptions import GlobalException

def custom_exception_handler(exc, context):
    """
    Custom exception handler for Django REST Framework.
    Formative structure matches Spring Boot's GlobalExceptionHandler.java.
    """
    if isinstance(exc, (AuthenticationFailed, NotAuthenticated, PermissionDenied)):
        # Replicating Spring Security raw JSON response on token error
        return Response(
            data={
                "msg": "Access Denied",
                "code": status.HTTP_403_FORBIDDEN,
                "status": "failure"
            },
            status=status.HTTP_403_FORBIDDEN
        )

    if isinstance(exc, ValidationError):
        errors_list = []
        if isinstance(exc.detail, dict):
            for field, messages in exc.detail.items():
                if isinstance(messages, list):
                    for msg in messages:
                        errors_list.append({field: str(msg)})
                else:
                    errors_list.append({field: str(messages)})
        elif isinstance(exc.detail, list):
            for msg in exc.detail:
                errors_list.append({"non_field_errors": str(msg)})
        else:
            errors_list.append({"error": str(exc.detail)})

        return ApiResponse(
            status=status.HTTP_400_BAD_REQUEST,
            message="Validation failed",
            result={"errors": errors_list}
        )

    if isinstance(exc, GlobalException):
        return ApiResponse(
            status=status.HTTP_400_BAD_REQUEST,
            message=exc.message,
            result=None
        )

    # Call DRF's default exception handler to check other DRF exception classes
    response = exception_handler(exc, context)

    if response is not None:
        # Wrap DRF standard exceptions in our ApiResponse envelope
        return ApiResponse(
            status=response.status_code,
            message=getattr(response, 'status_text', 'Error occurred'),
            result=response.data
        )

    return None

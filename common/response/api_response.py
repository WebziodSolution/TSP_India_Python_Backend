from rest_framework.response import Response

class ApiResponse(Response):
    """
    Standard API Response class to wrap all API responses.
    Matches the structure of ApiResponse.java.
    """
    def __init__(self, status: int, message: str, result=None, **kwargs):
        # We allow status code override via status parameter to match Spring Boot
        data = {
            "status": status,
            "message": message,
            "result": result
        }
        # In DRF, status is status_code. We pass status_code to Response's base class.
        super().__init__(data=data, status=status, **kwargs)

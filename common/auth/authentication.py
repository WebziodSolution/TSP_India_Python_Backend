import re
from django.utils.deprecation import MiddlewareMixin
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from common.models import Users, CompanyEmployee
from .jwt_token_util import JwtTokenUtil
import jwt
import logging
logger = logging.getLogger(__name__)
# List of public endpoints that bypass authentication
PUBLIC_URL_PATTERNS = [
    r'^/location',
    r'^/inout/clockInOut',
    r'^/getTimezones',
    r'^/uploadFile',
    r'^/user/uploadProfileImage',
    r'^/user/login',
    r'^/user/resetPassword',
    r'^/user/validateToken',
    r'^/user/generateResetLink',
    r'^/user/create',
    r'^/api/schema'
]


class JWTAuthentication(BaseAuthentication):
    """
    Custom DRF Authentication class translating Spring Security's JwtRequestFilter.java.
    """
    def __init__(self):
        self.jwt_util = JwtTokenUtil()

    def is_public_path(self, path):
        for pattern in PUBLIC_URL_PATTERNS:
            if re.search(pattern, path):
                return True
        return False

    def authenticate(self, request):
        path = request.path_info
        auth_header = request.headers.get('Authorization') or request.META.get('HTTP_AUTHORIZATION')

        # Fallback to bypass checks if it's a known public path and no header is provided
        if not auth_header:
            if self.is_public_path(path):
                return None
            logger.error("[DEBUG AUTH] No auth header and not public path. Access Denied.")
            raise AuthenticationFailed("Access Denied")

        if not auth_header.startswith('Bearer '):
            if self.is_public_path(path):
                logger.error("[DEBUG AUTH] Public path, invalid prefix, allowing.")
                return None
            logger.error("[DEBUG AUTH] Auth header does not start with Bearer. Access Denied.")
            raise AuthenticationFailed("Access Denied")

        token = auth_header[7:]
        try:
            # Extract claims using utility
            username = self.jwt_util.extract_username(token)
            company_id = self.jwt_util.extract_company_id(token)
            user_id = self.jwt_util.extract_user_id(token)

            if not username:
                raise AuthenticationFailed("Access Denied")

            # Try loading user from Users table first
            user = None
            try:
                if company_id == None:
                    user = Users.objects.filter(userId=user_id).first()
                else:
                    user = CompanyEmployee.objects.filter(employeeId=user_id).first()
            except Exception as e:
                pass

            if not user:
                raise AuthenticationFailed("Access Denied")

            # Build user data check dict
            user_data = {
                "userName": getattr(user, 'userName', ''),
                "email": getattr(user, 'email', '')
            }

            if not self.jwt_util.validate_token(token, user_data):
                logger.error("[DEBUG AUTH] validate_token returned False. Access Denied.")
                raise AuthenticationFailed("Access Denied")

            # Attach context metadata to the request for view controller access
            request.user_id = user_id
            request.company_id = company_id
            
            # Django views expect request.user to be authenticated
            return (user, token)

        except jwt.ExpiredSignatureError as e:
            logger.error(f"[DEBUG AUTH] Token expired: {e}")
            raise AuthenticationFailed("Access Denied")
        except jwt.InvalidTokenError as e:
            logger.error(f"[DEBUG AUTH] Invalid token: {e}")
            raise AuthenticationFailed("Access Denied")
        except Exception as e:
            logger.error(f"[DEBUG AUTH] General exception in authenticate: {e}")
            raise AuthenticationFailed("Access Denied")

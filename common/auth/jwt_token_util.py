import jwt
from datetime import datetime, timedelta
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

class JwtTokenUtil:
    """
    Utility class to handle JWT generation, claim extraction, and validation.
    Matches features of JwtTokenUtil.java.
    """
    def __init__(self):
        if not hasattr(settings, 'JWT_SECRET_KEY'):
            raise ImproperlyConfigured("JWT_SECRET_KEY is not configured in Django settings.")
        self.secret_key = settings.JWT_SECRET_KEY
        self.expiration_hours = getattr(settings, 'JWT_EXPIRATION_HOURS', 10)

    def generate_token(self, user: dict) -> str:
        """
        Generate a JWT token for a given user representation dictionary.
        """
        now = datetime.utcnow()
        payload = {
            "userId": str(user.get("userId", "")),
            "roleId": str(user.get("roleId", "")),
            "roleName": str(user.get("roleName", "")),
            "role": str(user.get("roleName", "")),  # Included both for compatibility
            "companyId": str(user.get("companyId", "")),
            "userName": str(user.get("userName", "")),
            "sub": str(user.get("userName", "")),  # subject matches userName in Spring Boot
            "iat": now,
            "exp": now + timedelta(hours=self.expiration_hours)
        }
        return jwt.encode(payload, self.secret_key, algorithm="HS256")

    def decode_token(self, token: str) -> dict:
        """
        Decodes token and returns claims. Raises jwt.InvalidTokenError or jwt.ExpiredSignatureError.
        """
        # pyjwt automatically checks expiration (exp) claim by default
        return jwt.decode(token, self.secret_key, algorithms=["HS256"])

    def extract_username(self, token: str) -> str:
        try:
            payload = self.decode_token(token)
            return payload.get("sub", "")
        except jwt.InvalidTokenError:
            # Replicating Java's silent failures where claims could raise or return default values
            return ""

    def extract_user_id(self, token: str) -> int:
        try:
            payload = self.decode_token(token)
            return int(payload.get("userId", 0))
        except (jwt.InvalidTokenError, ValueError):
            return 0

    def extract_member_role(self, token: str) -> str:
        try:
            payload = self.decode_token(token)
            return payload.get("role", payload.get("roleName", ""))
        except jwt.InvalidTokenError:
            return ""

    def extract_company_id(self, token: str) -> str:
        try:
            payload = self.decode_token(token)
            return payload.get("companyId", "")
        except jwt.InvalidTokenError:
            return ""

    def extract_expiration(self, token: str) -> datetime:
        payload = jwt.decode(token, self.secret_key, algorithms=["HS256"], options={"verify_exp": False})
        exp_timestamp = payload.get("exp")
        return datetime.utcfromtimestamp(exp_timestamp)

    def is_token_expired(self, token: str) -> bool:
        try:
            jwt.decode(token, self.secret_key, algorithms=["HS256"])
            return False
        except jwt.ExpiredSignatureError:
            return True
        except jwt.InvalidTokenError:
            return True

    def validate_token(self, token: str, user_data: dict) -> bool:
        try:
            payload = self.decode_token(token)
            username = payload.get("sub", "")
            matches = (username == user_data.get("email") or username == user_data.get("userName"))
            return matches
        except jwt.InvalidTokenError:
            return False

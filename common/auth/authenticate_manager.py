from django.contrib.auth.hashers import check_password
from common.models import Users, CompanyEmployee
from common.exception.exceptions import GlobalException

class CustomAuthenticateManager:
    """
    Service to authenticate credentials against Users and CompanyEmployee models.
    Matches features of CustomAuthenticateManager.java.
    """
    def authenticate(self, username, password, company_id=None):
        # 1. Search in Users table first (global users)
        user = None
        user_type = 'Users'
        
        try:
            user = Users.objects.filter(userName=username).first()
            if not user:
                user = Users.objects.filter(email=username).first()
        except Exception:
            pass

        # 2. Search in CompanyEmployee table (employees belonging to a company)
        if not user:
            user_type = 'CompanyEmployee'
            try:
                queryset = CompanyEmployee.objects.all()
                if company_id:
                    queryset = queryset.filter(companyDetails_id=company_id)
                
                # Check userName or email
                user = queryset.filter(userName=username).first()
                if not user:
                    user = queryset.filter(email=username).first()
            except Exception:
                pass

        if user is not None:
            # Replicating password verification
            # Java compares decryptPassword.equals(password) (plain text comparison).
            # To be production-ready and support both systems, we check both plain text
            # and Django's secure check_password hash.
            stored_pwd = getattr(user, 'password', '')
            password_valid = (stored_pwd == password) or check_password(password, stored_pwd)
            
            if password_valid:
                # Build representation map of the authenticated user
                # claims map in JwtTokenUtil: userId, roleId, roleName, companyId, userName
                role_name = ""
                role_id = ""
                
                if user_type == 'Users' and hasattr(user, 'role') and user.role:
                    role_name = getattr(user.role, 'roleName', '')
                    role_id = getattr(user.role, 'roleId', '')
                elif user_type == 'CompanyEmployee' and hasattr(user, 'roles') and user.roles:
                    role_name = getattr(user.roles, 'roleName', '')
                    role_id = getattr(user.roles, 'roleId', '')

                company_val = ""
                if user_type == 'CompanyEmployee' and hasattr(user, 'companyDetails') and user.companyDetails:
                    company_val = getattr(user.companyDetails, 'id', '')
                
                user_id = getattr(user, 'userId', None)
                if user_id is None:
                    user_id = getattr(user, 'employeeId', None)

                return {
                    "userId": str(user_id or ""),
                    "roleId": str(role_id or ""),
                    "roleName": str(role_name or ""),
                    "companyId": str(company_val or ""),
                    "userName": getattr(user, 'userName', ''),
                    "email": getattr(user, 'email', ''),
                    "type": user_type,
                    "object": user
                }
            else:
                raise GlobalException("Invalid Credentials")
        else:
            raise GlobalException("User Not Found")

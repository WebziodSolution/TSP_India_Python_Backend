import os
import re
import uuid
import time
import base64
import hmac
import hashlib
import logging
from django.db import models
from django.db.models import Q
from django.conf import settings
from django.contrib.auth.hashers import check_password
from common.models import (
    Users, CompanyEmployee, CompanyDetails, CompanyTheme,
    Department, Roles, Contractor, Locations
)
from common.exception.exceptions import GlobalException
from common.service import CommonService, get_file_directory
from common.auth.jwt_token_util import JwtTokenUtil
from common.serializers import UserSerializer, CompanyEmployeeSerializer
from common.specifications.employee_statement_specification import EmployeeStatementSpecification

logger = logging.getLogger(__name__)

class UserService:
    def __init__(self):
        self.common_service = CommonService()
        self.jwt_util = JwtTokenUtil()

    def get_all_users(self, company_id: int = None, department_ids: list = None, employee_ids: list = None) -> list:
        try:
            if company_id is not None or department_ids is not None or employee_ids is not None:
                spec_q = Q()
                if company_id is not None:
                    spec_q &= EmployeeStatementSpecification.has_company_id(company_id)
                if department_ids is not None:
                    spec_q &= EmployeeStatementSpecification.has_department_ids(department_ids)
                if employee_ids is not None:
                    spec_q &= EmployeeStatementSpecification.has_employee_ids(employee_ids)

                employees = CompanyEmployee.objects.filter(spec_q)
                return CompanyEmployeeSerializer(employees, many=True).data
            else:
                users_list = Users.objects.all()
                return [self.get_user_by_id(user.userId) for user in users_list]
        except Exception as e:
            logger.error(f"Error getting all users: {e}")
            raise Exception(str(e))

    def get_user_by_id(self, user_id: int) -> dict:
        try:
            user = Users.objects.filter(userId=user_id).first()
            if not user:
                raise Exception("User not found")
            
            user.departmentId = user.department_id if user.department else None
            user.roleId = user.role_id if user.role else None
            user.roleName = user.role.roleName if user.role else None
            user.contractorId = user.contractor_id if user.contractor else None
            user.userShiftId = user.userShift_id if user.userShift else None
            
            return UserSerializer(user).data
        except Exception as e:
            logger.error(f"Error getting user by id {user_id}: {e}")
            raise Exception(str(e))

    def create_user(self, user_dto: dict) -> dict:
        try:
            serializer = UserSerializer(data=user_dto)
            if not serializer.is_valid():
                raise GlobalException(f"Validation failed: {serializer.errors}")
            
            validated_data = serializer.validated_data
            dept_id = validated_data.get("departmentId")
            role_id = validated_data.get("roleId")
            
            department = Department.objects.filter(id=dept_id).first()
            if not department:
                raise Exception("Department not found")
                
            role = Roles.objects.filter(roleId=role_id).first()
            if not role:
                raise Exception("Role not found")
            
            user_name = validated_data.get("userName")
            if user_name:
                user_has = Users.objects.filter(userName=user_name).first()
                if user_has:
                    raise GlobalException("Username is already taken.")
            
            pin = validated_data.get("personalIdentificationNumber")
            if pin:
                user_has = Users.objects.filter(personalIdentificationNumber=pin).first()
                if user_has:
                    raise GlobalException("Personal identification number must be unique")
            
            users = Users(
                department=department,
                role=role,
                firstName=validated_data.get("firstName"),
                lastName=validated_data.get("lastName"),
                middleName=validated_data.get("middleName"),
                email=validated_data.get("email"),
                userName=user_name,
                phone=validated_data.get("phone"),
                password=validated_data.get("password"),
                gender=validated_data.get("gender"),
                hourlyRate=validated_data.get("hourlyRate"),
                personalIdentificationNumber=pin,
                address1=validated_data.get("address1"),
                address2=validated_data.get("address2"),
                city=validated_data.get("city"),
                zipCode=validated_data.get("zipCode"),
                country=validated_data.get("country"),
                state=validated_data.get("state"),
                birthDate=validated_data.get("birthDate"),
                emergencyContact=validated_data.get("emergencyContact"),
                contactPhone=validated_data.get("contactPhone"),
                relationship=validated_data.get("relationship"),
                profileImage=""
            )
            
            contractor_id = validated_data.get("contractorId")
            if contractor_id:
                contractor = Contractor.objects.filter(id=contractor_id).first()
                if not contractor:
                    raise Exception("Contractor not found")
                users.contractor = contractor
                
            users.save()
            return self.get_user_by_id(users.userId)
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            raise Exception(str(e))

    def update_user(self, user_id: int, user_dto: dict) -> dict:
        try:
            serializer = UserSerializer(data=user_dto)
            if not serializer.is_valid():
                raise GlobalException(f"Validation failed: {serializer.errors}")
            
            validated_data = serializer.validated_data
            
            user = Users.objects.filter(userId=user_id).first()
            if not user:
                raise Exception("User not found")
                
            dept_id = validated_data.get("departmentId")
            role_id = validated_data.get("roleId")
            
            department = Department.objects.filter(id=dept_id).first()
            if not department:
                raise Exception("Department not found")
                
            role = Roles.objects.filter(roleId=role_id).first()
            if not role:
                raise Exception("Role not found")
                
            user_name = validated_data.get("userName")
            if user_name:
                user_has = Users.objects.filter(userName=user_name).exclude(userId=user_id).first()
                if user_has:
                    raise GlobalException("Username is already taken.")
            
            user.department = department
            user.role = role
            user.firstName = validated_data.get("firstName")
            user.lastName = validated_data.get("lastName")
            user.middleName = validated_data.get("middleName")
            user.email = validated_data.get("email")
            user.userName = user_name
            user.phone = validated_data.get("phone")
            user.password = validated_data.get("password")
            user.gender = validated_data.get("gender")
            user.hourlyRate = validated_data.get("hourlyRate")
            user.personalIdentificationNumber = validated_data.get("personalIdentificationNumber")
            user.address1 = validated_data.get("address1")
            user.address2 = validated_data.get("address2")
            user.city = validated_data.get("city")
            user.zipCode = validated_data.get("zipCode")
            user.country = validated_data.get("country")
            user.state = validated_data.get("state")
            user.birthDate = validated_data.get("birthDate")
            user.emergencyContact = validated_data.get("emergencyContact")
            user.contactPhone = validated_data.get("contactPhone")
            user.relationship = validated_data.get("relationship")
            
            contractor_id = validated_data.get("contractorId")
            if contractor_id:
                contractor = Contractor.objects.filter(id=contractor_id).first()
                if not contractor:
                    raise Exception("Contractor not found")
                user.contractor = contractor
            else:
                user.contractor = None
                
            user.save()
            return self.get_user_by_id(user.userId)
        except Exception as e:
            logger.error(f"Error updating user: {e}")
            raise Exception(str(e))

    def delete_user(self, user_id: int) -> None:
        try:
            user = Users.objects.filter(userId=user_id).first()
            if not user:
                raise Exception("User not found")
            user.delete()
        except Exception as e:
            logger.error(f"Error deleting user: {e}")
            raise Exception(str(e))

    def user_login(self, login_dto: dict) -> dict:
        res_body = {}
        try:
            config_company_id = getattr(settings, 'companyId', '108108')
            req_company_id = str(login_dto.get("companyId", ""))
            user_name = login_dto.get("userName", "")
            password = login_dto.get("password", "")
            
            if req_company_id == str(config_company_id):
                user = Users.objects.filter(userName=user_name).first()
                if user:
                    if user.password == password or check_password(password, user.password):
                        data = {
                            "userId": user.userId,
                            "userName": user.userName,
                            "firstName": user.firstName,
                            "lastName": user.lastName,
                            "middleName": user.middleName,
                            "email": user.email,
                            "phone": user.phone,
                            "gender": user.gender,
                            "hourlyRate": user.hourlyRate,
                            "personalIdentificationNumber": user.personalIdentificationNumber,
                            "address1": user.address1,
                            "address2": user.address2,
                            "city": user.city,
                            "zipCode": user.zipCode,
                            "country": user.country,
                            "state": user.state,
                            "birthDate": user.birthDate,
                            "emergencyContact": user.emergencyContact,
                            "contactPhone": user.contactPhone,
                            "relationship": user.relationship,
                            "roleId": user.role.roleId if user.role else None,
                            "roleName": user.role.roleName if user.role else None,
                            "profileImage": user.profileImage,
                            "departmentId": user.department.id if user.department else None,
                        }
                        
                        user_map = {
                            "userId": str(user.userId),
                            "userName": user.userName,
                            "roleId": str(user.role.roleId if user.role else ""),
                            "roleName": user.role.roleName if user.role else "",
                            "companyId": str(config_company_id),
                        }
                        
                        token = self.jwt_util.generate_token(user_map)
                        res_body["token"] = token
                        res_body["data"] = data
                        return res_body
                    else:
                        res_body["errorType"] = "password"
                        res_body["error"] = "Invalid credentials."
                        return res_body
                else:
                    res_body["error"] = "Invalid credentials."
                    return res_body
            else:
                company_details = CompanyDetails.objects.filter(companyNo=req_company_id).first()
                if company_details and company_details.isActive == 1:
                    company_employee = CompanyEmployee.objects.filter(
                        companyDetails=company_details,
                        userName=user_name
                    ).first()
                    
                    if company_employee:
                        # Geofence check
                        role_name = company_employee.roles.roleName if company_employee.roles else ""
                        if role_name not in ["Admin", "Owner"] and company_employee.checkGeofence == 1:
                            comp_loc = company_employee.companyLocation or ""
                            if comp_loc:
                                comp_loc_clean = comp_loc.replace('[', '').replace(']', '')
                                parts = [p.strip() for p in comp_loc_clean.split(',') if p.strip()]
                                for p in parts:
                                    location = Locations.objects.filter(id=int(p)).first()
                                    if location:
                                        if not location.geofenceId:
                                            res_body["error"] = "Geofence data is missing or incomplete for one or more locations. Please contact your administrator to configure geofencing for your company's locations before proceeding."
                                            return res_body
                                    else:
                                        res_body["error"] = "Geofence data is missing or incomplete for one or more locations. Please contact your administrator to configure geofencing for your company's locations before proceeding."
                                        return res_body
                            else:
                                res_body["error"] = "Login failed due to internal error."
                                return res_body
                        
                        if company_employee.password == password or check_password(password, company_employee.password):
                            theme_id = None
                            company_theme = CompanyTheme.objects.filter(companyDetails=company_details).first()
                            if company_theme:
                                theme_id = company_theme.id
                            
                            company_employee_dto = {
                                "employeeId": company_employee.employeeId,
                                "userName": company_employee.userName,
                                "firstName": company_employee.firstName,
                                "lastName": company_employee.lastName,
                                "middleName": company_employee.middleName,
                                "email": company_employee.email,
                                "phone": company_employee.phone,
                                "gender": company_employee.gender,
                                "hourlyRate": company_employee.hourlyRate,
                                "address1": company_employee.address1,
                                "address2": company_employee.address2,
                                "city": company_employee.city,
                                "zipCode": company_employee.zipCode,
                                "country": company_employee.country,
                                "state": company_employee.state,
                                "dob": str(company_employee.dob) if company_employee.dob else None,
                                "emergencyContact": company_employee.emergencyContact,
                                "contactPhone": company_employee.contactPhone,
                                "relationship": company_employee.relationship,
                                "roleId": company_employee.roles.roleId if company_employee.roles else None,
                                "roleName": company_employee.roles.roleName if company_employee.roles else None,
                                "profileImage": company_employee.profileImage,
                                "companyId": company_employee.companyDetails.id if company_employee.companyDetails else None,
                                "departmentName": company_employee.department.departmentName if company_employee.department else None,
                                "themeId": theme_id
                            }
                            
                            user_map = {
                                "userId": str(company_employee.employeeId),
                                "userName": company_employee.userName,
                                "roleId": str(company_employee.roles.roleId if company_employee.roles else ""),
                                "roleName": str(company_employee.roles.roleId if company_employee.roles else ""),
                                "companyId": str(company_employee.companyDetails.id if company_employee.companyDetails else ""),
                            }
                            
                            token = self.jwt_util.generate_token(user_map)
                            res_body["token"] = token
                            res_body["data"] = company_employee_dto
                            return res_body
                        else:
                            res_body["error"] = "Invalid credentials."
                            return res_body
                    else:
                        res_body["error"] = f"User not found for company Id {company_details.companyNo}"
                        return res_body
                else:
                    res_body["error"] = "Company Id is not valid"
                    return res_body
        except Exception as e:
            logger.error(f"Login internal error: {e}")
            res_body["error"] = "Login failed due to internal error."
        return res_body

    def generate_reset_link(self, email: str, user_name: str, id_str: str) -> bool:
        try:
            config_company_id = getattr(settings, 'companyId', '108108')
            if str(id_str) == str(config_company_id):
                user = Users.objects.filter(email=email, userName=user_name).first()
                if user and user.userId:
                    return self._generate_token(user.userId, email, config_company_id)
            else:
                company_employee = CompanyEmployee.objects.filter(
                    companyDetails__companyNo=id_str,
                    userName=user_name,
                    email=email
                ).first()
                if company_employee:
                    return self._generate_token(company_employee.employeeId, email, id_str)
            return False
        except Exception as e:
            logger.error(f"Error generating reset link: {e}")
            raise Exception(f"Error generating reset link: {str(e)}")

    def _generate_token(self, user_id: int, email: str, company_no: str) -> bool:
        current_timestamp = int(time.time() * 1000)
        token_uuid = str(uuid.uuid4())
        data = f"{company_no}:{user_id}:{token_uuid}:{current_timestamp}"
        
        secret_key = "your-very-secret-key"
        mac = hmac.new(secret_key.encode('utf-8'), data.encode('utf-8'), hashlib.sha256)
        hmac_bytes = mac.digest()
        
        hmac_b64 = base64.urlsafe_b64encode(hmac_bytes).decode('utf-8').rstrip('=')
        
        raw_token = f"{data}:{hmac_b64}"
        token_encoded = base64.urlsafe_b64encode(raw_token.encode('utf-8')).decode('utf-8').rstrip('=')
        
        site_url = getattr(settings, 'siteUrl', 'http://localhost:3000/')
        if not site_url.endswith('/'):
            site_url += '/'
        route = f"{site_url}reset-pin/{token_encoded}"
        
        subject = "Reset Your Password - TimeSheetsPro"
        body = (
            f"Hello,\n\n"
            f"We received a request to reset your password for your TimeSheetsPro account.\n"
            f"Please click the link below to reset your PIN:\n\n"
            f"{route}\n\n"
            f"If you did not request this, you can safely ignore this email.\n\n"
            f"Thank you,\n"
            f"TimeSheetsPro Support Team"
        )
        
        return self.common_service.send_email(email, subject, body)

    def validate_token(self, token: str) -> dict:
        try:
            token_padded = token
            rem = len(token_padded) % 4
            if rem > 0:
                token_padded += '=' * (4 - rem)
            
            decoded_token = base64.urlsafe_b64decode(token_padded.encode('utf-8')).decode('utf-8')
            parts = decoded_token.split(":")
            if len(parts) != 5:
                return {
                    "message": "Invalid token structure",
                    "status": 400
                }
            
            company_no = parts[0]
            user_id_str = parts[1]
            token_uuid = parts[2]
            timestamp = int(parts[3])
            provided_hmac_b64 = parts[4]
            
            user = Users.objects.filter(userId=int(user_id_str)).first()
            if not user:
                company_employee = CompanyEmployee.objects.filter(employeeId=int(user_id_str)).first()
                if not company_employee:
                    return {
                        "message": "User not found",
                        "status": 404
                    }
            
            current_timestamp = int(time.time() * 1000)
            if current_timestamp - timestamp > 180 * 1000:
                return {
                    "message": "Token is expired.",
                    "status": 404
                }
            
            data = f"{company_no}:{user_id_str}:{token_uuid}:{timestamp}"
            secret_key = "your-very-secret-key"
            mac = hmac.new(secret_key.encode('utf-8'), data.encode('utf-8'), hashlib.sha256)
            expected_hmac = mac.digest()
            
            provided_hmac_pad = provided_hmac_b64
            rem_hmac = len(provided_hmac_pad) % 4
            if rem_hmac > 0:
                provided_hmac_pad += '=' * (4 - rem_hmac)
            
            provided_hmac_bytes = base64.urlsafe_b64decode(provided_hmac_pad.encode('utf-8'))
            
            if hmac.compare_digest(expected_hmac, provided_hmac_bytes):
                return {
                    "message": "Token is valid",
                    "status": 200,
                    "userId": int(user_id_str)
                }
            return None
        except Exception as e:
            logger.error(f"Error validating token: {e}")
            raise Exception(f"Error validating token: {str(e)}")

    def reset_password(self, reset_password_dto: dict) -> dict:
        res_body = {}
        try:
            token = reset_password_dto.get("token", "")
            token_padded = token
            rem = len(token_padded) % 4
            if rem > 0:
                token_padded += '=' * (4 - rem)
            
            decoded_token = base64.urlsafe_b64decode(token_padded.encode('utf-8')).decode('utf-8')
            parts = decoded_token.split(":")
            if len(parts) != 5:
                return {
                    "message": "Invalid token structure",
                    "status": 400
                }
            
            company_no = parts[0]
            user_id_str = parts[1]
            
            config_company_id = getattr(settings, 'companyId', '108108')
            if str(company_no) == str(config_company_id):
                user = Users.objects.filter(userId=int(user_id_str)).first()
                if not user:
                    raise Exception("User not found")
                
                curr_pwd = reset_password_dto.get("currentPassword")
                if curr_pwd is not None:
                    if not (user.password == curr_pwd or check_password(curr_pwd, user.password)):
                        res_body["passwordNotMatch"] = "Current pin is wrong."
                        return res_body
                
                user.password = reset_password_dto.get("password")
                user.save()
                res_body["success"] = "Pin change successfully."
                return res_body
            else:
                company_employee = CompanyEmployee.objects.filter(employeeId=int(user_id_str)).first()
                if not company_employee:
                    raise Exception("Company not found")
                
                curr_pwd = reset_password_dto.get("currentPassword")
                if curr_pwd is not None:
                    if not (company_employee.password == curr_pwd or check_password(curr_pwd, company_employee.password)):
                        res_body["passwordNotMatch"] = "Current pin is wrong."
                        return res_body
                
                company_employee.password = reset_password_dto.get("password")
                company_employee.save()
                res_body["success"] = "Pin change successfully."
                return res_body
        except Exception as e:
            logger.error(f"Error resetting password: {e}")
            raise Exception(f"Error resetPassword: {str(e)}")

    def upload_profile_image(self, user_id: int, image_path: str) -> str:
        try:
            self.delete_profile_image(user_id)
            user = Users.objects.filter(userId=user_id).first()
            if not user:
                raise Exception("User not found")
            
            updated_path = self.common_service.update_file_location_for_profile(image_path, user_id, "profileImages")
            if updated_path == "Error":
                return "Error"
            
            user.profileImage = updated_path
            user.save()
            return updated_path
        except Exception as e:
            logger.error(f"Error uploading profile image: {e}")
            raise Exception(f"Error uploadProfileImage: {str(e)}")

    def delete_profile_image(self, user_id: int) -> bool:
        try:
            user = Users.objects.filter(userId=user_id).first()
            if not user:
                raise Exception("User not found")
            
            user.profileImage = ""
            user.save()
            
            file_dir = get_file_directory()
            existing_image_path = os.path.join(file_dir, str(user_id), "profileImages")
            if os.path.exists(existing_image_path):
                self.common_service.delete_directory_recursively(existing_image_path)
                return True
            return False
        except Exception as e:
            logger.error(f"Error deleting profile image: {e}")
            raise Exception(f"Error deleteProfileImage: {str(e)}")

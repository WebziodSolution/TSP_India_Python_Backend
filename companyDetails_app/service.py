import os
import logging
from django.utils import timezone
from common.models import (
    CompanyDetails, CompanyTheme, Locations, CompanyEmployee, CompanyEmployeeRoles, CompanyRoleModuleActions, CompanyModuleActions
)
from common.exception.exceptions import GlobalException
from common.service import CommonService, get_file_directory
from common.specifications.company_specification import CompanySpecification

logger = logging.getLogger(__name__)

class CompanyDetailsService:
    def __init__(self):
        self.common_service = CommonService()

    def search_companies(self, name: str, active: int) -> list:
        try:            
            spec_q = CompanySpecification.search_by_name(name)
            if active in [0, 1]:
                spec_q &= CompanySpecification.is_active(active == 1)
                
            companies = CompanyDetails.objects.filter(spec_q)
            
            simplified_list = []
            for company in companies:
                simplified_list.append({
                    "id": company.id,
                    "companyName": company.companyName,
                    "companyLogo": company.companyLogo or ""
                })
            return simplified_list
        except Exception as e:
            logger.error(f"Error search_companies: {e}")
            raise Exception(str(e))

    def get_all_company_details(self, active: int) -> list:
        try:
            if active == 2:
                companies = CompanyDetails.objects.all()
            else:
                companies = CompanyDetails.objects.filter(isActive=active)
                
            company_details_list = []
            for company in companies:
                company_details_list.append({
                    "id": company.id,
                    "companyName": company.companyName,
                    "companyLogo": company.companyLogo or ""
                })
            return company_details_list
        except Exception as e:
            logger.error(f"Error get_all_company_details: {e}")
            raise Exception(str(e))

    def get_company_details(self, company_id: int) -> dict:
        try:
            company = CompanyDetails.objects.filter(id=company_id).first()
            if not company:
                raise Exception("Company details not found")
                
            locations = Locations.objects.filter(companyDetails=company)
            locations_dto_list = []
            if locations:
                for loc in locations:
                    locations_dto_list.append({
                        "companyId": loc.companyDetails.id if loc.companyDetails else None,
                        "id": loc.id,
                        "city": loc.city or "",
                        "state": loc.state or "",
                        "country": loc.country or "",
                        "address1": loc.address1 or "",
                        "address2": loc.address2 or "",
                        "employeeCount": loc.employeeCount or 0,
                        "locationName": loc.locationName or "",
                        "externalId": loc.externalId or "",
                        "zipCode": loc.zipCode or "",
                        "geofenceId": loc.geofenceId or "",
                        "isActive": loc.isActive or 0
                })
                
            register_date_str = self.common_service.convert_date_to_string(company.registerDate)
            
            company_dto = {
                "id": company.id,
                "companyNo": company.companyNo or "",
                "companyName": company.companyName or "",
                "ein": company.ein or "",
                "organizationType": company.organizationType or "",
                "dba": company.dba or "",
                "email": company.email or "",
                "industryName": company.industryName or "",
                "phone": company.phone or "",
                "websiteUrl": company.websiteUrl or "",
                "registerDate": register_date_str or "",
                "companyLogo": company.companyLogo or "",
                "locations": locations_dto_list,
                "autoTimeInAfterHours": company.autoTimeInAfterHours or ""
            }
            return company_dto
        except Exception as e:
            logger.error(f"Error get_company_details: {e}")
            raise Exception(str(e))

    def create_company_details(self, company_dto: dict, step: str) -> dict:
        try:            
            if step != "1":
                raise GlobalException("Server Error")
                
            company_name = company_dto.get("companyName")
            ein = company_dto.get("ein")
            
            is_exists = CompanyDetails.objects.filter(companyName=company_name).first()
            if not is_exists and ein:
                is_exists = CompanyDetails.objects.filter(ein=ein).first()
            if is_exists:
                raise GlobalException(f"{company_name} is already registered")
                
            if ein:
                is_ein_exists = CompanyDetails.objects.filter(ein=ein).first()
                if is_ein_exists:
                    raise GlobalException(f"GST number {ein} is already registered")
                    
            company = CompanyDetails(
                companyNo=company_dto.get("companyNo") or "",
                companyName=company_name or "",
                dba=company_dto.get("dba") or "",
                companyLogo=company_dto.get("companyLogo") or "",
                email=company_dto.get("email") or "",
                phone=company_dto.get("phone") or "",
                industryName=company_dto.get("industryName") or "",
                websiteUrl=company_dto.get("websiteUrl") or "",
                isActive=1,
                registerDate=timezone.now(),
                ein=ein or "",
                organizationType=company_dto.get("organizationType") or "",
                autoTimeInAfterHours="20:00"
            )
            company.save()
            
            theme = CompanyTheme(
                companyDetails=company,
                primaryColor="#666cff",
                textColor="#262b43",
                sideNavigationBgColor="#ffffff",
                headerBgColor="#ffffff",
                contentBgColor="#F5F5F7",
                iconColor="#262b43"
            )
            theme.save()
            
            return self.get_company_details(company.id)
        except Exception as e:
            logger.error(f"Error create_company_details: {e}")
            raise e

    def create_company_employee_role(self, role_dto: dict) -> dict:
        try:
            company_id = role_dto.get("companyId")
            role_name = role_dto.get("roleName")
            
            company = CompanyDetails.objects.filter(id=company_id).first()
            if not company:
                raise Exception("Company not found")
                
            role = CompanyEmployeeRoles.objects.filter(companyDetails=company, roleName=role_name).first()
            if not role:
                role = CompanyEmployeeRoles(
                    companyDetails=company,
                    roleName=role_name
                )
                role.save()
                
            roles_actions_data = role_dto.get("rolesActions", {})
            if roles_actions_data and isinstance(roles_actions_data, dict):
                functionalities = roles_actions_data.get("functionalities", [])
                for func in functionalities:
                    modules = func.get("modules", [])
                    for mod in modules:
                        module_id = mod.get("moduleId")
                        role_assigned_actions = mod.get("roleAssignedActions", [])
                        
                        for act in role_assigned_actions:
                            action_id = None
                            if isinstance(act, dict):
                                action_id = act.get("actionId") or act.get("id")
                            elif isinstance(act, (int, str)):
                                action_id = int(act)
                                
                            if action_id is not None:
                                module_action = CompanyModuleActions.objects.filter(
                                    module_id=module_id,
                                    action_id=action_id
                                ).first()
                                if module_action:
                                    CompanyRoleModuleActions.objects.get_or_create(
                                        role=role,
                                        moduleActions=module_action
                                    )
            return {
                "roleId": role.roleId,
                "companyId": company.id,
                "roleName": role.roleName
            }
        except Exception as e:
            logger.error(f"Error creating company employee role: {e}")
            raise Exception(str(e))

    def create_employee_from_tsp(self, emp_dto: dict) -> dict:
        try:
            company = CompanyDetails.objects.filter(id=emp_dto.get("companyId")).first()
            if not company:
                raise Exception("Company not found")
                
            role = CompanyEmployeeRoles.objects.filter(roleId=emp_dto.get("roleId")).first()
            
            username = emp_dto.get("userName")
            if CompanyEmployee.objects.filter(companyDetails=company, userName=username).exists():
                raise GlobalException("Username is already taken.")
                
            employee = CompanyEmployee(
                companyDetails=company,
                roles=role,
                userName=username,
                firstName=emp_dto.get("firstName"),
                lastName=emp_dto.get("lastName"),
                email=emp_dto.get("email"),
                password=emp_dto.get("password"),
                phone=emp_dto.get("phone"),
                address1=emp_dto.get("address1"),
                city=emp_dto.get("city"),
                state=emp_dto.get("state"),
                country=emp_dto.get("country"),
                isActive=1,
                checkGeofence=0
            )
            employee.save()
            return {"employeeId": employee.employeeId}
        except Exception as e:
            logger.error(f"Error create_employee_from_tsp: {e}")
            raise e

    def update_company_details(self, company_id: int, company_dto: dict, step: str) -> dict:
        try:
            company = CompanyDetails.objects.filter(id=company_id).first()
            if not company:
                raise Exception("Company details not found")
                
            if step == "1":
                company_name = company_dto.get("companyName")
                ein = company_dto.get("ein")
                
                is_exists = CompanyDetails.objects.filter(companyName=company_name).exclude(id=company_id).first()
                if not is_exists and ein:
                    is_exists = CompanyDetails.objects.filter(ein=ein).exclude(id=company_id).first()
                if is_exists:
                    raise GlobalException(f"{company_name} is already registered")
                    
                if ein:
                    is_ein_exists = CompanyDetails.objects.filter(ein=ein).exclude(id=company_id).first()
                    if is_ein_exists:
                        raise GlobalException(f"GST number {ein} is already registered")
                        
                company.companyName = company_name or ""
                company.companyNo = company_dto.get("companyNo") or ""
                company.dba = company_dto.get("dba") or ""
                company.email = company_dto.get("email") or ""
                company.phone = company_dto.get("phone") or ""
                company.industryName = company_dto.get("industryName") or ""
                company.websiteUrl = company_dto.get("websiteUrl") or ""
                company.ein = ein or ""
                company.organizationType = company_dto.get("organizationType") or ""
                company.isActive = 1
                company.save()
                
                return self.get_company_details(company.id)
                
            elif step == "3":
                deleted_ids = company_dto.get("deletedEmployeeId", [])
                if deleted_ids:
                    for emp_id in deleted_ids:
                        CompanyEmployee.objects.filter(employeeId=emp_id).delete()
                        
                employees = company_dto.get("employees", [])
                if employees:
                    roles_list = CompanyEmployeeRoles.objects.filter(companyDetails=company)
                    
                    if not roles_list.exists():
                        roles_dto_list = company_dto.get("roles", [])
                        for emp_data in employees:
                            for role_data in roles_dto_list:
                                if role_data.get("roleName") != emp_data.get("roleName"):
                                    self.create_company_employee_role({
                                        "companyId": company.id,
                                        "roleName": role_data.get("roleName"),
                                        "rolesActions": role_data.get("rolesActions")
                                    })
                            role_payload = {
                                "companyId": company.id,
                                "roleName": emp_data.get("roleName")
                            }
                            matching_role = next((r for r in roles_dto_list if r.get("roleName") == emp_data.get("roleName")), None)
                            if not matching_role and roles_dto_list:
                                matching_role = roles_dto_list[-1]
                            if matching_role:
                                role_payload["rolesActions"] = matching_role.get("rolesActions")
                                
                            created_role_info = self.create_company_employee_role(role_payload)
                            
                            self.create_employee_from_tsp({
                                "companyId": company.id,
                                "roleId": created_role_info["roleId"],
                                "firstName": emp_data.get("firstName"),
                                "lastName": emp_data.get("lastName"),
                                "email": emp_data.get("email"),
                                "phone": emp_data.get("phone"),
                                "address1": emp_data.get("address1"),
                                "city": emp_data.get("city"),
                                "state": emp_data.get("state"),
                                "country": emp_data.get("country"),
                                "userName": emp_data.get("userName"),
                                "password": emp_data.get("password")
                            })
                    else:
                        for emp_data in employees:
                            role_name = emp_data.get("roleName")
                            role = CompanyEmployeeRoles.objects.filter(companyDetails=company, roleName=role_name).first()
                            if not role:
                                role_dto_list = company_dto.get("roles", [])
                                matching_role = next((r for r in role_dto_list if r.get("roleName") == role_name), None)
                                role_payload = {"companyId": company.id, "roleName": role_name}
                                if matching_role:
                                    role_payload["rolesActions"] = matching_role.get("rolesActions")
                                created_role_info = self.create_company_employee_role(role_payload)
                                role_id = created_role_info["roleId"]
                            else:
                                role_id = role.roleId
                                
                            self.create_employee_from_tsp({
                                "companyId": company.id,
                                "roleId": role_id,
                                "firstName": emp_data.get("firstName"),
                                "lastName": emp_data.get("lastName"),
                                "email": emp_data.get("email"),
                                "phone": emp_data.get("phone"),
                                "address1": emp_data.get("address1"),
                                "city": emp_data.get("city"),
                                "state": emp_data.get("state"),
                                "country": emp_data.get("country"),
                                "userName": emp_data.get("userName"),
                                "password": emp_data.get("password")
                            })
                            
                return self.get_company_details(company.id)
            else:
                return None
        except Exception as e:
            logger.error(f"Error update_company_details: {e}")
            raise e

    def delete_company_details(self, company_id: int) -> None:
        try:
            company = CompanyDetails.objects.filter(id=company_id).first()
            if not company:
                raise Exception("Company details not found")
            company.delete()
        except Exception as e:
            logger.error(f"Error delete_company_details: {e}")
            raise Exception(str(e))

    def upload_company_logo(self, company_id: int, image_path: str) -> str:
        try:
            self.delete_company_logo(company_id)
            company = CompanyDetails.objects.filter(id=company_id).first()
            if not company:
                raise Exception("Company not found")
                
            updated_path = self.common_service.update_file_location_for_profile(image_path, company_id, "companyLogo")
            if updated_path == "Error":
                return "Error"
            else:
                company.companyLogo = updated_path
                company.save()
                return updated_path
        except Exception as e:
            logger.error(f"Error upload_company_logo: {e}")
            raise Exception(str(e))

    def delete_company_logo(self, company_id: int) -> bool:
        try:
            company = CompanyDetails.objects.filter(id=company_id).first()
            if not company:
                raise Exception("Company not found")
                
            file_dir = get_file_directory()
            existing_image_path = os.path.join(file_dir, str(company_id), "companyLogo")
            if os.path.exists(existing_image_path):
                self.common_service.delete_directory_recursively(existing_image_path)
                company.companyLogo = ""
                company.save()
                return True
            return False
        except Exception as e:
            logger.error(f"Error delete_company_logo: {e}")
            raise Exception(str(e))

    def get_last_company(self) -> str:
        try:
            last_company = CompanyDetails.objects.order_by('-id').first()
            if last_company:
                return last_company.companyNo
            return None
        except Exception as e:
            logger.error(f"Error get_last_company: {e}")
            raise Exception(str(e))

    def update_auto_time_in_after_hours(self, company_id: int, data: str) -> None:
        try:
            company = CompanyDetails.objects.filter(id=company_id).first()
            if not company:
                raise Exception("Company not found")
            company.autoTimeInAfterHours = data
            company.save()
        except Exception as e:
            logger.error(f"Error update_auto_time_in_after_hours: {e}")
            raise Exception(str(e))

    def get_auto_time_in_after_hours(self, company_id: int) -> str:
        try:
            company = CompanyDetails.objects.filter(id=company_id).first()
            if not company:
                raise Exception("Company not found")
            return company.autoTimeInAfterHours
        except Exception as e:
            logger.error(f"Error get_auto_time_in_after_hours: {e}")
            raise Exception(str(e))

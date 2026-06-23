import os
import logging
import calendar
from datetime import datetime
from django.db import transaction
from django.db.models import Q
from common.models import (
    CompanyEmployee,
    CompanyDetails,
    CompanyEmployeeRoles,
    Department,
    EmployeeType,
    CompanyShift,
    UserInOut,
    WeeklyOff,
    HolidayTemplates,
    OvertimeRules,
    EmployeeBackAccountInfo,
    SalaryStatementHistory,
)
from common.service import CommonService, get_file_directory
from companyEmployeeRole_app.service import CompanyEmployeeRoleService

logger = logging.getLogger(__name__)

class CompanyEmployeeService:
    def __init__(self):
        self.common_service = CommonService()
        self.company_employee_role_service = CompanyEmployeeRoleService()

    def get_reports(self, company_id: int, type_str: str, month: int, user_time_zone: str) -> list:
        try:
            year = datetime.now().year
            # Java does `month + 1`, which is because Java Calendar/frontend may pass 0-indexed month
            month_val = int(month) + 1
            
            _, last_day = calendar.monthrange(year, month_val)
            start_date = datetime(year, month_val, 1).date()
            end_date = datetime(year, month_val, last_day).date()

            # Filter UserInOut entries matching date range and companyId
            user_in_outs = UserInOut.objects.filter(
                companyDetails_id=company_id,
                createdOn__date__range=(start_date, end_date),
                isSalaryGenerate=1
            )

            # Collect unique keys: employeeId | companyId
            unique_keys = set()
            for u in user_in_outs:
                if u.user and u.companyDetails:
                    unique_keys.add(f"{u.user.employeeId}|{u.companyDetails.id}")

            results = []
            for key in unique_keys:
                parts = key.split("|")
                employee_id = int(parts[0])
                comp_id = int(parts[1])

                history_list = SalaryStatementHistory.objects.filter(
                    employeeId=employee_id,
                    companyDetails_id=comp_id
                )

                for history in history_list:
                    company_employee = CompanyEmployee.objects.filter(employeeId=employee_id).first()
                    if not company_employee:
                        continue

                    record = {
                        "userName": history.employeeName or (f"{company_employee.firstName} {company_employee.lastName}" if company_employee.firstName else company_employee.userName)
                    }

                    if company_employee.isPf and type_str == "PF":
                        record["employee_pf_amount"] = history.totalPfAmount
                        record["employer_pf_amount"] = history.totalPfAmount
                        record["total_amount"] = (history.totalPfAmount or 0) * 2
                        results.append(record)
                    elif company_employee.isPt and type_str == "PT":
                        record["pt_amount"] = company_employee.ptAmount
                        results.append(record)

            return results
        except Exception as e:
            logger.error(f"Error in get_reports: {e}")
            raise Exception(str(e))

    def get_all_employee_list_by_company_id(self, company_id: int) -> list:
        try:
            employees = CompanyEmployee.objects.filter(companyDetails_id=company_id).order_by('employeeId')
            response = []
            for emp in employees:
                response.append({
                    "employeeId": emp.employeeId,
                    "userName": f"{emp.firstName or ''} {emp.lastName or ''}".strip() or emp.userName
                })
            return response
        except Exception as e:
            logger.error(f"Error in get_all_employee_list_by_company_id: {e}")
            raise Exception(str(e))

    def get_all_employee_by_company_id(self, company_id: int) -> list:
        try:
            # Query finds contractors/employees for company
            employees = CompanyEmployee.objects.filter(companyDetails_id=company_id).order_by('employeeId')
            return [self.get_employee(emp.employeeId) for emp in employees]
        except Exception as e:
            logger.error(f"Error in get_all_employee_by_company_id: {e}")
            raise Exception(str(e))

    def get_employee(self, id: int) -> dict:
        try:
            employee = CompanyEmployee.objects.filter(employeeId=id).first()
            if not employee:
                raise Exception("Employee not found")

            bank_info = EmployeeBackAccountInfo.objects.filter(companyEmployee_id=id).first()
            bank_account_id = bank_info.id if bank_info else None

            shift_dto = None
            if employee.companyShift:
                shift_dto = {
                    "id": employee.companyShift.id,
                    "companyId": employee.companyShift.companyDetails.id if employee.companyShift.companyDetails else None,
                    "shiftName": employee.companyShift.shiftName,
                    "shiftType": employee.companyShift.shiftType,
                    "startTime": employee.companyShift.startTime,
                    "endTime": employee.companyShift.endTime,
                    "hours": employee.companyShift.hours,
                    "totalHours": employee.companyShift.totalHours
                }

            role_dto = None
            if employee.roles:
                role_dto = self.company_employee_role_service.get_role(employee.roles.roleId)

            dto = {
                "employeeId": employee.employeeId,
                "companyId": employee.companyDetails.id if employee.companyDetails else None,
                "roleId": employee.roles.roleId if employee.roles else None,
                "userName": employee.userName,
                "firstName": employee.firstName,
                "lastName": employee.lastName,
                "email": employee.email,
                "password": employee.password,
                "phone": employee.phone,
                "emergencyPhone": employee.emergencyPhone,
                "altPhone": employee.altPhone,
                "profileImage": employee.profileImage,
                "gender": employee.gender,
                "dob": employee.dob.strftime("%Y-%m-%d") if employee.dob else None,
                "zipCode": employee.zipCode,
                "city": employee.city,
                "state": employee.state,
                "country": employee.country,
                "hourlyRate": employee.hourlyRate,
                "address1": employee.address1,
                "address2": employee.address2,
                "roleName": employee.roles.roleName if employee.roles else None,
                "middleName": employee.middleName,
                "emergencyContact": employee.emergencyContact,
                "contactPhone": employee.contactPhone,
                "relationship": employee.relationship,
                "departmentId": employee.department.id if employee.department else None,
                "departmentName": employee.department.departmentName if employee.department else None,
                "employeeTypeId": employee.employeeType.id if employee.employeeType else None,
                "employeeTypeName": employee.employeeType.name if employee.employeeType else None,
                "payPeriod": employee.payPeriod,
                "hiredDate": employee.hiredDate.strftime("%Y-%m-%d") if employee.hiredDate else None,
                "bankAccountId": bank_account_id,
                "isActive": employee.isActive,
                "shiftId": employee.companyShift.id if employee.companyShift else None,
                "companyLocation": employee.companyLocation,
                "checkGeofence": employee.checkGeofence,
                "embedding": employee.embedding,
                "bloodGroup": employee.bloodGroup,
                "aadharImage": employee.aadharImage,
                "isPf": employee.isPf,
                "pfType": employee.pfType,
                "pfPercentage": employee.pfPercentage,
                "pfAmount": employee.pfAmount,
                "isPt": employee.isPt,
                "ptAmount": employee.ptAmount,
                "basicSalary": employee.basicSalary,
                "grossSalary": employee.grossSalary,
                "canteenType": employee.canteenType,
                "canteenAmount": employee.canteenAmount,
                "otId": employee.overtimeRules.id if employee.overtimeRules else None,
                "lunchBreak": employee.lunchBreak,
                "workingHoursIncludeLunch": employee.workingHoursIncludeLunch,
                "weeklyOffId": employee.weeklyOff.id if employee.weeklyOff else None,
                "holidayTemplateId": employee.holidayTemplates.id if employee.holidayTemplates else None,
                "earlyExitPenaltyRule": employee.earlyExitPenaltyRule,
                "lateEntryPenaltyRule": employee.lateEntryPenaltyRule,
                "companyShiftDto": shift_dto,
                "companyEmployeeRolesDto": role_dto,
            }
            return dto
        except Exception as e:
            logger.error(f"Error in get_employee: {e}")
            raise Exception(str(e))

    @transaction.atomic
    def create_employee(self, dto: dict) -> dict:
        try:
            company_id = dto.get("companyId")
            company = CompanyDetails.objects.filter(id=company_id).first()
            if not company:
                raise Exception("Company not found")

            role_id = dto.get("roleId")
            role = CompanyEmployeeRoles.objects.filter(roleId=role_id).first()
            if not role:
                raise Exception("Role not found")

            department_id = dto.get("departmentId")
            department = None
            if department_id:
                department = Department.objects.filter(id=department_id).first()
                if not department:
                    raise Exception("Department not found")

            employee_type_id = dto.get("employeeTypeId")
            employee_type = None
            if employee_type_id:
                employee_type = EmployeeType.objects.filter(id=employee_type_id).first()
                if not employee_type:
                    raise Exception("Employee type not found")

            shift_id = dto.get("shiftId")
            shift = None
            if shift_id:
                shift = CompanyShift.objects.filter(id=shift_id).first()
                if not shift:
                    raise Exception("Shift not found")

            is_exists = CompanyEmployee.objects.filter(companyDetails_id=company_id, userName=dto.get("userName")).first()
            if is_exists:
                raise Exception("User name is already taken")

            employee = CompanyEmployee()

            if dto.get("hiredDate"):
                employee.hiredDate = self.common_service.convert_string_to_date(dto.get("hiredDate"))
            if dto.get("dob"):
                employee.dob = self.common_service.convert_string_to_date(dto.get("dob"))

            ot_id = dto.get("otId")
            if ot_id:
                overtime_rules = OvertimeRules.objects.filter(id=ot_id).first()
                if not overtime_rules:
                    raise Exception("Overtime rule not found")
                employee.overtimeRules = overtime_rules

            weekly_off_id = dto.get("weeklyOffId")
            if weekly_off_id:
                weekly_off = WeeklyOff.objects.filter(id=weekly_off_id).first()
                if not weekly_off:
                    raise Exception("Weekly off not found")
                employee.weeklyOff = weekly_off
            else:
                # Find default weekly off
                weekly_off = WeeklyOff.objects.filter(companyDetails_id=company_id, isDefault=1).first()
                employee.weeklyOff = weekly_off

            holiday_template_id = dto.get("holidayTemplateId")
            if holiday_template_id:
                holiday_template = HolidayTemplates.objects.filter(id=holiday_template_id).first()
                if not holiday_template:
                    raise Exception("Holiday template not found")
                employee.holidayTemplates = holiday_template

            employee.companyDetails = company
            employee.roles = role
            employee.department = department
            employee.employeeType = employee_type
            employee.companyShift = shift

            # Map fields from dto
            exclude_fields = {
                "employeeId", "companyId", "roleId", "departmentId",
                "employeeTypeId", "shiftId", "weeklyOffId", "holidayTemplateId", "otId",
                "dob", "hiredDate", "companyDetails", "roles", "department",
                "employeeType", "companyShift", "weeklyOff", "holidayTemplates", "overtimeRules"
            }
            for field, value in dto.items():
                if field not in exclude_fields and hasattr(employee, field):
                    setattr(employee, field, value)

            employee.save()
            return self.get_employee(employee.employeeId)
        except Exception as e:
            logger.error(f"Error in create_employee: {e}")
            raise Exception(str(e))

    @transaction.atomic
    def update_employee(self, id: int, dto: dict) -> dict:
        try:
            employee = CompanyEmployee.objects.filter(employeeId=id).first()
            if not employee:
                raise Exception("Employee not found")

            company_id = dto.get("companyId")
            company = CompanyDetails.objects.filter(id=company_id).first()
            if not company:
                raise Exception("Company not found")

            role_id = dto.get("roleId")
            role = CompanyEmployeeRoles.objects.filter(roleId=role_id).first()
            if not role:
                raise Exception("Role not found")

            department_id = dto.get("departmentId")
            department = None
            if department_id:
                department = Department.objects.filter(id=department_id).first()
                if not department:
                    raise Exception("Department not found")

            employee_type_id = dto.get("employeeTypeId")
            employee_type = None
            if employee_type_id:
                employee_type = EmployeeType.objects.filter(id=employee_type_id).first()
                if not employee_type:
                    raise Exception("Employee type not found")

            shift_id = dto.get("shiftId")
            shift = None
            if shift_id:
                shift = CompanyShift.objects.filter(id=shift_id).first()
                if not shift:
                    raise Exception("Shift not found")

            is_exists = CompanyEmployee.objects.filter(companyDetails_id=company_id, userName=dto.get("userName")).first()
            if is_exists and is_exists.employeeId != employee.employeeId:
                raise Exception("User name is already taken")

            if dto.get("hiredDate"):
                employee.hiredDate = self.common_service.convert_string_to_date(dto.get("hiredDate"))
            else:
                employee.hiredDate = None

            if dto.get("dob"):
                employee.dob = self.common_service.convert_string_to_date(dto.get("dob"))
            else:
                employee.dob = None

            ot_id = dto.get("otId")
            if ot_id:
                overtime_rules = OvertimeRules.objects.filter(id=ot_id).first()
                if not overtime_rules:
                    raise Exception("Overtime rule not found")
                employee.overtimeRules = overtime_rules
            else:
                employee.overtimeRules = None

            weekly_off_id = dto.get("weeklyOffId")
            if weekly_off_id:
                weekly_off = WeeklyOff.objects.filter(id=weekly_off_id).first()
                if not weekly_off:
                    raise Exception("Weekly off not found")
                employee.weeklyOff = weekly_off
            else:
                # Find default weekly off
                weekly_off = WeeklyOff.objects.filter(companyDetails_id=company_id, isDefault=1).first()
                employee.weeklyOff = weekly_off

            holiday_template_id = dto.get("holidayTemplateId")
            if holiday_template_id:
                holiday_template = HolidayTemplates.objects.filter(id=holiday_template_id).first()
                if not holiday_template:
                    raise Exception("Holiday template not found")
                employee.holidayTemplates = holiday_template
            else:
                employee.holidayTemplates = None

            employee.companyDetails = company
            employee.roles = role
            employee.department = department
            employee.employeeType = employee_type
            employee.companyShift = shift

            # Map fields from dto
            exclude_fields = {
                "employeeId", "companyId", "roleId", "departmentId",
                "employeeTypeId", "shiftId", "weeklyOffId", "holidayTemplateId", "otId",
                "dob", "hiredDate", "companyDetails", "roles", "department",
                "employeeType", "companyShift", "weeklyOff", "holidayTemplates", "overtimeRules"
            }
            for field, value in dto.items():
                if field not in exclude_fields and hasattr(employee, field):
                    setattr(employee, field, value)

            employee.save()
            return self.get_employee(employee.employeeId)
        except Exception as e:
            logger.error(f"Error in update_employee: {e}")
            raise Exception(str(e))

    def delete_employee(self, id: int) -> None:
        try:
            employee = CompanyEmployee.objects.filter(employeeId=id).first()
            if not employee:
                raise Exception("Employee not found")
            
            company_id = employee.companyDetails.id if employee.companyDetails else None
            if company_id:
                self.delete_employee_profile(company_id, id)
                
            employee.delete()
        except Exception as e:
            logger.error(f"Error in delete_employee: {e}")
            raise Exception(str(e))

    def upload_employee_profile(self, company_id: int, employee_id: int, image_path: str) -> str:
        try:
            self.delete_employee_profile(company_id, employee_id)
            employee = CompanyEmployee.objects.filter(employeeId=employee_id).first()
            if not employee:
                raise Exception("Employee not found")

            updated_path = self.common_service.update_file_location_for_profile(
                image_path,
                company_id,
                f"employeeProfile/{employee_id}"
            )
            if updated_path == "Error":
                return "Error"
            else:
                employee.profileImage = updated_path
                employee.save()
                return updated_path
        except Exception as e:
            logger.error(f"Error in upload_employee_profile: {e}")
            raise Exception(str(e))

    def delete_employee_profile(self, company_id: int, employee_id: int) -> bool:
        try:
            employee = CompanyEmployee.objects.filter(employeeId=employee_id).first()
            if not employee:
                raise Exception("Employee not found")

            file_dir = get_file_directory()
            existing_image_path = os.path.join(file_dir, str(company_id), "employeeProfile", str(employee_id))
            if os.path.exists(existing_image_path):
                self.common_service.delete_directory_recursively(existing_image_path)
                employee.profileImage = ""
                employee.save()
                return True
            return False
        except Exception as e:
            logger.error(f"Error in delete_employee_profile: {e}")
            raise Exception(str(e))

    def upload_employee_aadhar_image(self, company_id: int, employee_id: int, image_path: str) -> str:
        try:
            # We call delete_employee_aadhar_image to cleanup prior Aadhar uploads
            self.delete_employee_aadhar_image(company_id, employee_id)
            employee = CompanyEmployee.objects.filter(employeeId=employee_id).first()
            if not employee:
                raise Exception("Employee not found")

            updated_path = self.common_service.update_file_location_for_profile(
                image_path,
                company_id,
                f"employeeProfile/aadharImage/{employee_id}"
            )
            if updated_path == "Error":
                return "Error"
            else:
                employee.aadharImage = updated_path
                employee.save()
                return updated_path
        except Exception as e:
            logger.error(f"Error in upload_employee_aadhar_image: {e}")
            raise Exception(str(e))

    def delete_employee_aadhar_image(self, company_id: int, employee_id: int) -> bool:
        try:
            employee = CompanyEmployee.objects.filter(employeeId=employee_id).first()
            if not employee:
                raise Exception("Employee not found")

            file_dir = get_file_directory()
            existing_image_path = os.path.join(file_dir, str(company_id), "employeeProfile", "aadharImage", str(employee_id))
            if os.path.exists(existing_image_path):
                self.common_service.delete_directory_recursively(existing_image_path)
                employee.aadharImage = ""
                employee.save()
                return True
            return False
        except Exception as e:
            logger.error(f"Error in delete_employee_aadhar_image: {e}")
            raise Exception(str(e))

    def get_last_user_id(self) -> int:
        try:
            last_emp = CompanyEmployee.objects.all().order_by('-employeeId').first()
            if not last_emp:
                return 0
            return last_emp.employeeId
        except Exception as e:
            logger.error(f"Error in get_last_user_id: {e}")
            raise Exception(str(e))

    @transaction.atomic
    def create_employee_from_tsp(self, employee_dto: dict) -> dict:
        try:
            role_id = employee_dto.get("roleId")
            company_id = employee_dto.get("companyId")
            
            # Check if there are roles for the company
            roles_exist = CompanyEmployeeRoles.objects.filter(companyDetails_id=company_id).exists()
            if not roles_exist:
                roles_list = employee_dto.get("roles", [])
                for role_data in roles_list:
                    if role_data.get("roleName") != employee_dto.get("roleName"):
                        roles_dto = {
                            "companyId": company_id,
                            "roleName": role_data.get("roleName"),
                            "rolesActions": role_data.get("rolesActions")
                        }
                        self.company_employee_role_service.create_role(roles_dto)
                
                # Create the final role matching TSP's roleName
                roles_actions = roles_list[-1].get("rolesActions") if roles_list else None
                roles_dto = {
                    "companyId": company_id,
                    "roleName": employee_dto.get("roleName"),
                    "rolesActions": roles_actions
                }
                created_role = self.company_employee_role_service.create_role(roles_dto)
                role_id = created_role.get("roleId")

            company_details = CompanyDetails.objects.filter(id=company_id).first()
            if not company_details:
                raise Exception("Company not found")

            company_employee_roles = CompanyEmployeeRoles.objects.filter(roleId=role_id).first()
            if not company_employee_roles:
                raise Exception("Role not found")

            is_exists = CompanyEmployee.objects.filter(companyDetails_id=company_id, userName=employee_dto.get("userName")).first()
            if is_exists:
                raise Exception("User name is already taken")

            employee = CompanyEmployee()
            employee.companyDetails = company_details
            employee.roles = company_employee_roles
            employee.lateEntryPenaltyRule = True
            employee.earlyExitPenaltyRule = True

            # Map fields
            exclude_fields = {
                "employeeId", "companyId", "roleId", "departmentId",
                "employeeTypeId", "shiftId", "weeklyOffId", "holidayTemplateId", "otId",
                "dob", "hiredDate", "companyDetails", "roles", "department",
                "employeeType", "companyShift", "weeklyOff", "holidayTemplates", "overtimeRules"
            }
            for field, value in employee_dto.items():
                if field not in exclude_fields and hasattr(employee, field):
                    setattr(employee, field, value)

            employee.save()
            employee_dto["employeeId"] = employee.employeeId
            return employee_dto
        except Exception as e:
            logger.error(f"Error in create_employee_from_tsp: {e}")
            raise Exception(str(e))

    @transaction.atomic
    def update_employee_from_tsp(self, id: int, employee_dto: dict) -> dict:
        try:
            employee = CompanyEmployee.objects.filter(employeeId=id).first()
            if not employee:
                raise Exception("CompanyEmployee not found")

            company_id = employee_dto.get("companyId")
            company_details = CompanyDetails.objects.filter(id=company_id).first()
            if not company_details:
                raise Exception("Company not found")

            role_id = employee_dto.get("roleId")
            company_employee_roles = CompanyEmployeeRoles.objects.filter(roleId=role_id).first()
            if not company_employee_roles:
                raise Exception("Role not found")

            is_exists = CompanyEmployee.objects.filter(companyDetails_id=company_id, userName=employee_dto.get("userName")).first()
            if is_exists and is_exists.userName != employee.userName:
                raise Exception("User name is already taken")

            employee.companyDetails = company_details
            employee.roles = company_employee_roles
            employee.lateEntryPenaltyRule = True
            employee.earlyExitPenaltyRule = True

            # Map fields
            exclude_fields = {
                "employeeId", "companyId", "roleId", "departmentId",
                "employeeTypeId", "shiftId", "weeklyOffId", "holidayTemplateId", "otId",
                "dob", "hiredDate", "companyDetails", "roles", "department",
                "employeeType", "companyShift", "weeklyOff", "holidayTemplates", "overtimeRules"
            }
            for field, value in employee_dto.items():
                if field not in exclude_fields and hasattr(employee, field):
                    setattr(employee, field, value)

            employee.save()
            employee_dto["employeeId"] = employee.employeeId
            return employee_dto
        except Exception as e:
            logger.error(f"Error in update_employee_from_tsp: {e}")
            raise Exception(str(e))

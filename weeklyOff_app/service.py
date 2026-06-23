import logging
from common.models import WeeklyOff, CompanyDetails, CompanyEmployee

logger = logging.getLogger(__name__)

class WeeklyOffService:

    def _convert_model_to_dto(self, w: WeeklyOff) -> dict:
        assigned_emp_ids = self.getAssignedEmployees(w.id)
        return {
            "id": w.id,
            "name": w.name,
            "description": w.description,
            "isDefault": w.isDefault,
            "sundayAll": w.sundayAll,
            "sunday1st": w.sunday1st,
            "sunday2nd": w.sunday2nd,
            "sunday3rd": w.sunday3rd,
            "sunday4th": w.sunday4th,
            "sunday5th": w.sunday5th,
            "mondayAll": w.mondayAll,
            "monday1st": w.monday1st,
            "monday2nd": w.monday2nd,
            "monday3rd": w.monday3rd,
            "monday4th": w.monday4th,
            "monday5th": w.monday5th,
            "tuesdayAll": w.tuesdayAll,
            "tuesday1st": w.tuesday1st,
            "tuesday2nd": w.tuesday2nd,
            "tuesday3rd": w.tuesday3rd,
            "tuesday4th": w.tuesday4th,
            "tuesday5th": w.tuesday5th,
            "wednesdayAll": w.wednesdayAll,
            "wednesday1st": w.wednesday1st,
            "wednesday2nd": w.wednesday2nd,
            "wednesday3rd": w.wednesday3rd,
            "wednesday4th": w.wednesday4th,
            "wednesday5th": w.wednesday5th,
            "thursdayAll": w.thursdayAll,
            "thursday1st": w.thursday1st,
            "thursday2nd": w.thursday2nd,
            "thursday3rd": w.thursday3rd,
            "thursday4th": w.thursday4th,
            "thursday5th": w.thursday5th,
            "fridayAll": w.fridayAll,
            "friday1st": w.friday1st,
            "friday2nd": w.friday2nd,
            "friday3rd": w.friday3rd,
            "friday4th": w.friday4th,
            "friday5th": w.friday5th,
            "saturdayAll": w.saturdayAll,
            "saturday1st": w.saturday1st,
            "saturday2nd": w.saturday2nd,
            "saturday3rd": w.saturday3rd,
            "saturday4th": w.saturday4th,
            "saturday5th": w.saturday5th,
            "companyId": w.companyDetails.id if w.companyDetails else None,
            "createdBy": w.companyEmployee.employeeId if w.companyEmployee else None,
            "createdByUsername": w.companyEmployee.userName if w.companyEmployee else None,
            "assignedEmployeeIds": assigned_emp_ids
        }

    def assignEmployees(self, employee_ids: list, weekly_off_id: int, remove_employee_ids: list) -> bool:
        try:
            if employee_ids:
                weekly_off = WeeklyOff.objects.filter(id=weekly_off_id).first()
                if not weekly_off:
                    raise Exception("Weekly off not found")
                for emp_id in employee_ids:
                    emp = CompanyEmployee.objects.filter(employeeId=emp_id).first()
                    if not emp:
                        raise Exception("Employee not found with ID: " + str(emp_id))
                    emp.weeklyOff = weekly_off
                    emp.save()
            if remove_employee_ids:
                for emp_id in remove_employee_ids:
                    emp = CompanyEmployee.objects.filter(employeeId=emp_id).first()
                    if not emp:
                        raise Exception("Employee not found with ID: " + str(emp_id))
                    emp.weeklyOff = None
                    emp.save()
            return True
        except Exception as e:
            logger.error(f"Error assignEmployees: {e}")
            raise Exception(str(e))

    def getAllByCompany(self, company_id: int) -> list:
        try:
            weekly_offs = WeeklyOff.objects.filter(companyDetails_id=company_id)
            return [self.getById(w.id) for w in weekly_offs]
        except Exception as e:
            logger.error(f"Error getAllByCompany: {e}")
            raise Exception(str(e))

    def getById(self, id: int) -> dict:
        try:
            w = WeeklyOff.objects.filter(id=id).first()
            if not w:
                raise Exception("Weekly off not found")
            return self._convert_model_to_dto(w)
        except Exception as e:
            logger.error(f"Error getById: {e}")
            raise Exception(str(e))

    def _has_any_flag(self, dto: dict) -> bool:
        flags = [
            "sundayAll", "sunday1st", "sunday2nd", "sunday3rd", "sunday4th", "sunday5th",
            "mondayAll", "monday1st", "monday2nd", "monday3rd", "monday4th", "monday5th",
            "tuesdayAll", "tuesday1st", "tuesday2nd", "tuesday3rd", "tuesday4th", "tuesday5th",
            "wednesdayAll", "wednesday1st", "wednesday2nd", "wednesday3rd", "wednesday4th", "wednesday5th",
            "thursdayAll", "thursday1st", "thursday2nd", "thursday3rd", "thursday4th", "thursday5th",
            "fridayAll", "friday1st", "friday2nd", "friday3rd", "friday4th", "friday5th",
            "saturdayAll", "saturday1st", "saturday2nd", "saturday3rd", "saturday4th", "saturday5th"
        ]
        return any(dto.get(flag) is True for flag in flags)

    def create(self, dto: dict) -> dict:
        try:
            if not self._has_any_flag(dto):
                raise Exception("At least one weekly off must be selected")
                
            is_exists = WeeklyOff.objects.filter(companyDetails_id=dto.get("companyId"), name=dto.get("name")).first()
            if is_exists:
                raise Exception("Template name already exists")

            company = CompanyDetails.objects.filter(id=dto.get("companyId")).first()
            if not company:
                raise Exception("Company not found")

            employee = CompanyEmployee.objects.filter(employeeId=dto.get("createdBy")).first()
            if not employee:
                raise Exception("Employee not found")

            weekly_off = WeeklyOff()
            weekly_off.companyDetails = company
            weekly_off.companyEmployee = employee
            weekly_off.isDefault = 0
            
            # Map flags
            for key, val in dto.items():
                if hasattr(weekly_off, key) and key not in ["id", "isDefault", "companyId", "createdBy", "createdByUsername", "assignedEmployeeIds"]:
                    setattr(weekly_off, key, val)
                    
            weekly_off.save()
            dto["id"] = weekly_off.id
            return dto
        except Exception as e:
            logger.error(f"Error create weeklyOff: {e}")
            raise Exception(str(e))

    def update(self, id: int, dto: dict) -> dict:
        try:
            is_exists = WeeklyOff.objects.filter(name=dto.get("name")).exclude(id=id).first()
            if is_exists:
                raise Exception("Template name already exists")
                
            if not self._has_any_flag(dto):
                raise Exception("At least one weekly off must be selected")

            weekly_off = WeeklyOff.objects.filter(id=id).first()
            if not weekly_off:
                raise Exception("Weekly off not found")

            company = CompanyDetails.objects.filter(id=dto.get("companyId")).first()
            if not company:
                raise Exception("Company not found")

            employee = CompanyEmployee.objects.filter(employeeId=dto.get("createdBy")).first()
            if not employee:
                raise Exception("Employee not found")

            weekly_off.companyDetails = company
            weekly_off.companyEmployee = employee
            
            for key, val in dto.items():
                if hasattr(weekly_off, key) and key not in ["id", "isDefault", "companyId", "createdBy", "createdByUsername", "assignedEmployeeIds"]:
                    setattr(weekly_off, key, val)
                    
            weekly_off.save()
            dto["id"] = weekly_off.id
            return dto
        except Exception as e:
            logger.error(f"Error update weeklyOff: {e}")
            raise Exception(str(e))

    def delete(self, id: int) -> None:
        try:
            weekly_off = WeeklyOff.objects.filter(id=id).first()
            if not weekly_off:
                raise Exception("Weekly off not found")
            weekly_off.delete()
        except Exception as e:
            logger.error(f"Error delete weeklyOff: {e}")
            raise Exception(str(e))

    def assignDefaultWeeklyOff(self, id: int) -> None:
        try:
            weekly_off = WeeklyOff.objects.filter(id=id).first()
            if not weekly_off:
                raise Exception("Weekly off not found")
                
            weekly_off.isDefault = 0 if weekly_off.isDefault == 1 else 1
            
            default_weekly_off = WeeklyOff.objects.filter(isDefault=1).exclude(id=id).first()
            if default_weekly_off:
                default_weekly_off.isDefault = 0
                default_weekly_off.save()
                
            weekly_off.save()
            
            company_employees = CompanyEmployee.objects.filter(companyDetails_id=weekly_off.companyDetails.id)
            for emp in company_employees:
                if emp.employeeType and emp.employeeType.name == "Salaried":
                    emp.weeklyOff = weekly_off
                    emp.save()
        except Exception as e:
            logger.error(f"Error assignDefaultWeeklyOff: {e}")
            raise Exception(str(e))

    def getAssignedEmployees(self, weekly_off_id: int) -> list:
        try:
            employees = CompanyEmployee.objects.filter(weeklyOff_id=weekly_off_id)
            return [emp.employeeId for emp in employees]
        except Exception as e:
            logger.error(f"Error getAssignedEmployees: {e}")
            raise Exception(str(e))

import logging
from common.models import EmployeeLeaveMaster, CompanyEmployee, LeaveType
from common.serializers import EmployeeleavemasterSerializer

logger = logging.getLogger(__name__)

class EmployeeLeaveMasterService:
    def get_employee_leave_master(self, id: int) -> dict:
        try:
            elm = EmployeeLeaveMaster.objects.filter(id=id).first()
            if not elm:
                raise Exception("Employee leave master not found")
            dto = {
                "id": elm.id,
                "employeeId": elm.companyEmployee.employeeId if elm.companyEmployee else None,
                "leaveTypeId": elm.leaveType.id if elm.leaveType else None,
                "totalLeave": elm.totalLeave,
                "usedLeave": elm.usedLeave
            }
            return EmployeeleavemasterSerializer(dto).data
        except Exception as e:
            logger.error(f"Error in get_employee_leave_master: {e}")
            raise Exception(str(e))

    def get_all_employee_leave_masters(self, company_id: int) -> list:
        try:
            entities = EmployeeLeaveMaster.objects.filter(companyEmployee__companyDetails_id=company_id).order_by('id')
            dto_list = []
            for elm in entities:
                dto_list.append(self.get_employee_leave_master(elm.id))
            return dto_list
        except Exception as e:
            logger.error(f"Error in get_all_employee_leave_masters: {e}")
            raise Exception(str(e))

    def get_employee_leave_masters_by_employee(self, employee_id: int) -> list:
        try:
            entities = EmployeeLeaveMaster.objects.filter(companyEmployee_id=employee_id).order_by('id')
            dto_list = []
            for elm in entities:
                dto_list.append(self.get_employee_leave_master(elm.id))
            return dto_list
        except Exception as e:
            logger.error(f"Error in get_employee_leave_masters_by_employee: {e}")
            raise Exception(str(e))

    def create_employee_leave_master(self, dto: dict) -> dict:
        try:
            serializer = EmployeeleavemasterSerializer(data=dto)
            if not serializer.is_valid():
                raise Exception(f"Validation failed: {serializer.errors}")
                
            validated_data = serializer.validated_data
            employee_id = validated_data.get("employeeId")
            employee = None
            if employee_id is not None:
                employee = CompanyEmployee.objects.filter(employeeId=employee_id).first()
                if not employee:
                    raise Exception("Employee not found")
                    
            leave_type_id = validated_data.get("leaveTypeId")
            leave_type = None
            if leave_type_id is not None:
                leave_type = LeaveType.objects.filter(id=leave_type_id).first()
                if not leave_type:
                    raise Exception("LeaveType not found")
                    
            elm = EmployeeLeaveMaster(
                companyEmployee=employee,
                leaveType=leave_type,
                totalLeave=validated_data.get("totalLeave"),
                usedLeave=validated_data.get("usedLeave")
            )
            elm.save()
            return self.get_employee_leave_master(elm.id)
        except Exception as e:
            logger.error(f"Error in create_employee_leave_master: {e}")
            raise Exception(str(e))

    def update_employee_leave_master(self, id: int, dto: dict) -> dict:
        try:
            elm = EmployeeLeaveMaster.objects.filter(id=id).first()
            if not elm:
                raise Exception("Employee leave master not found")
                
            serializer = EmployeeleavemasterSerializer(data=dto)
            if not serializer.is_valid():
                raise Exception(f"Validation failed: {serializer.errors}")
                
            validated_data = serializer.validated_data
            employee_id = validated_data.get("employeeId")
            employee = None
            if employee_id is not None:
                employee = CompanyEmployee.objects.filter(employeeId=employee_id).first()
                if not employee:
                    raise Exception("Employee not found")
                    
            leave_type_id = validated_data.get("leaveTypeId")
            leave_type = None
            if leave_type_id is not None:
                leave_type = LeaveType.objects.filter(id=leave_type_id).first()
                if not leave_type:
                    raise Exception("LeaveType not found")
                    
            elm.companyEmployee = employee
            elm.leaveType = leave_type
            elm.totalLeave = validated_data.get("totalLeave")
            elm.usedLeave = validated_data.get("usedLeave")
            elm.save()
            return self.get_employee_leave_master(elm.id)
        except Exception as e:
            logger.error(f"Error in update_employee_leave_master: {e}")
            raise Exception(str(e))

    def delete_employee_leave_master(self, id: int) -> None:
        try:
            elm = EmployeeLeaveMaster.objects.filter(id=id).first()
            if not elm:
                raise Exception("Employee leave master not found")
            elm.delete()
        except Exception as e:
            logger.error(f"Error in delete_employee_leave_master: {e}")
            raise Exception(str(e))

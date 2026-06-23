import logging
from common.models import EmploymentInfo, CompanyEmployee
from common.serializers import EmploymentInfoSerializer
from common.service import CommonService

logger = logging.getLogger(__name__)

class EmploymentInfoService:
    def __init__(self):
        self.common_service = CommonService()

    def get_employment_info_by_id(self, id: int) -> dict:
        try:
            entity = EmploymentInfo.objects.filter(id=id).first()
            if not entity:
                raise Exception("EmploymentInfo not found")
            dto = {
                "id": entity.id,
                "workPhone": entity.workPhone,
                "ext": entity.ext,
                "workEmail": entity.workEmail,
                "hireDate": self.common_service.convert_date_to_string(entity.hireDate),
                "status": entity.status,
                "paidPension": entity.paidPension,
                "statutoryEmployee": entity.statutoryEmployee,
                "exclusionIndicator": entity.exclusionIndicator,
                "keyEmployeeIndicator": entity.keyEmployeeIndicator,
                "hce": entity.hce,
                "unionIndicator": entity.unionIndicator,
                "eligibilityIndicator": entity.eligibilityIndicator,
                "employeeId": entity.companyEmployee.employeeId if entity.companyEmployee else None
            }
            return EmploymentInfoSerializer(dto).data
        except Exception as e:
            logger.error(f"Error in get_employment_info_by_id: {e}")
            raise Exception(str(e))

    def get_all_employment_info(self) -> list:
        try:
            entities = EmploymentInfo.objects.all().order_by('id')
            dto_list = []
            for entity in entities:
                dto_list.append(self.get_employment_info_by_id(entity.id))
            return dto_list
        except Exception as e:
            logger.error(f"Error in get_all_employment_info: {e}")
            raise Exception(str(e))

    def create_employment_info(self, dto: dict) -> dict:
        try:
            serializer = EmploymentInfoSerializer(data=dto)
            if not serializer.is_valid():
                raise Exception(f"Validation failed: {serializer.errors}")
                
            validated_data = serializer.validated_data
            employee_id = validated_data.get("employeeId")
            employee = CompanyEmployee.objects.filter(employeeId=employee_id).first()
            if not employee:
                raise Exception("Employee not found")
                
            hire_date = self.common_service.convert_string_to_date(validated_data.get("hireDate"))
            
            entity = EmploymentInfo(
                companyEmployee=employee,
                workPhone=validated_data.get("workPhone"),
                ext=validated_data.get("ext"),
                workEmail=validated_data.get("workEmail"),
                hireDate=hire_date,
                status=validated_data.get("status"),
                paidPension=validated_data.get("paidPension"),
                statutoryEmployee=validated_data.get("statutoryEmployee"),
                exclusionIndicator=validated_data.get("exclusionIndicator"),
                keyEmployeeIndicator=validated_data.get("keyEmployeeIndicator"),
                hce=validated_data.get("hce"),
                unionIndicator=validated_data.get("unionIndicator"),
                eligibilityIndicator=validated_data.get("eligibilityIndicator")
            )
            entity.save()
            return self.get_employment_info_by_id(entity.id)
        except Exception as e:
            logger.error(f"Error in create_employment_info: {e}")
            raise Exception(str(e))

    def update_employment_info(self, id: int, dto: dict) -> dict:
        try:
            entity = EmploymentInfo.objects.filter(id=id).first()
            if not entity:
                raise Exception("EmploymentInfo not found")
                
            serializer = EmploymentInfoSerializer(data=dto)
            if not serializer.is_valid():
                raise Exception(f"Validation failed: {serializer.errors}")
                
            validated_data = serializer.validated_data
            employee_id = validated_data.get("employeeId")
            employee = CompanyEmployee.objects.filter(employeeId=employee_id).first()
            if not employee:
                raise Exception("Employee not found")
                
            hire_date = self.common_service.convert_string_to_date(validated_data.get("hireDate"))
            
            entity.companyEmployee = employee
            entity.workPhone = validated_data.get("workPhone")
            entity.ext = validated_data.get("ext")
            entity.workEmail = validated_data.get("workEmail")
            entity.hireDate = hire_date
            entity.status = validated_data.get("status")
            entity.paidPension = validated_data.get("paidPension")
            entity.statutoryEmployee = validated_data.get("statutoryEmployee")
            entity.exclusionIndicator = validated_data.get("exclusionIndicator")
            entity.keyEmployeeIndicator = validated_data.get("keyEmployeeIndicator")
            entity.hce = validated_data.get("hce")
            entity.unionIndicator = validated_data.get("unionIndicator")
            entity.eligibilityIndicator = validated_data.get("eligibilityIndicator")
            
            entity.save()
            return self.get_employment_info_by_id(entity.id)
        except Exception as e:
            logger.error(f"Error in update_employment_info: {e}")
            raise Exception(str(e))

    def delete_employment_info(self, id: int) -> None:
        try:
            entity = EmploymentInfo.objects.filter(id=id).first()
            if not entity:
                raise Exception("EmploymentInfo not found")
            entity.delete()
        except Exception as e:
            logger.error(f"Error in delete_employment_info: {e}")
            raise Exception(str(e))

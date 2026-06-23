import logging
from common.models import EmployeeType
from common.serializers import EmployeeTypeSerializer

logger = logging.getLogger(__name__)

class EmployeeTypeService:
    def get_employee_type(self, id: int) -> dict:
        try:
            employee_type = EmployeeType.objects.filter(id=id).first()
            if not employee_type:
                raise Exception("Type not found")
            dto = {
                "id": employee_type.id,
                "name": employee_type.name
            }
            return EmployeeTypeSerializer(dto).data
        except Exception as e:
            logger.error(f"Error in get_employee_type: {e}")
            raise Exception(str(e))

    def get_all_employee_types(self) -> list:
        try:
            employee_types = EmployeeType.objects.all().order_by('id')
            dto_list = []
            for et in employee_types:
                dto_list.append(self.get_employee_type(et.id))
            return dto_list
        except Exception as e:
            logger.error(f"Error in get_all_employee_types: {e}")
            raise Exception(str(e))

    def create_employee_type(self, employee_type_dto: dict) -> dict:
        try:
            serializer = EmployeeTypeSerializer(data=employee_type_dto)
            if not serializer.is_valid():
                raise Exception(f"Validation failed: {serializer.errors}")
                
            validated_data = serializer.validated_data
            employee_type = EmployeeType(
                name=validated_data.get("name")
            )
            employee_type.save()
            return self.get_employee_type(employee_type.id)
        except Exception as e:
            logger.error(f"Error in create_employee_type: {e}")
            raise Exception(str(e))

    def update_employee_type(self, id: int, employee_type_dto: dict) -> dict:
        try:
            employee_type = EmployeeType.objects.filter(id=id).first()
            if not employee_type:
                raise Exception("Type not found")
                
            serializer = EmployeeTypeSerializer(data=employee_type_dto)
            if not serializer.is_valid():
                raise Exception(f"Validation failed: {serializer.errors}")
                
            validated_data = serializer.validated_data
            employee_type.name = validated_data.get("name")
            employee_type.save()
            return self.get_employee_type(employee_type.id)
        except Exception as e:
            logger.error(f"Error in update_employee_type: {e}")
            raise Exception(str(e))

    def delete_employee_type(self, id: int) -> None:
        try:
            employee_type = EmployeeType.objects.filter(id=id).first()
            if not employee_type:
                raise Exception("Type not found")
            employee_type.delete()
        except Exception as e:
            logger.error(f"Error in delete_employee_type: {e}")
            raise Exception(str(e))

import logging
from django.db import transaction
from common.models import Deductions, CompanyEmployee
from common.serializers import DeductionsSerializer

logger = logging.getLogger(__name__)

class DeductionsService:
    def find_by_id(self, id: int) -> dict:
        try:
            deductions = Deductions.objects.filter(id=id).first()
            if not deductions:
                raise Exception("Deductions not found!")
            dto = {
                "id": deductions.id,
                "employeeId": deductions.companyEmployee.employeeId if deductions.companyEmployee else None,
                "type": deductions.type,
                "label": deductions.label,
                "amount": deductions.amount
            }
            return DeductionsSerializer(dto).data
        except Exception as e:
            logger.error(f"Error in find_by_id: {e}")
            raise Exception(str(e))

    def find_by_employee_id(self, employee_id: int) -> list:
        try:
            deductions = Deductions.objects.filter(companyEmployee_id=employee_id).order_by('id')
            deductions_dto_list = []
            for deduction in deductions:
                deductions_dto_list.append(self.find_by_id(deduction.id))
            return deductions_dto_list
        except Exception as e:
            logger.error(f"Error in find_by_employee_id: {e}")
            raise Exception(str(e))

    @transaction.atomic
    def save_deductions(self, deductions_dto_list: list) -> None:
        try:
            if deductions_dto_list:
                for dto in deductions_dto_list:
                    serializer = DeductionsSerializer(data=dto)
                    if not serializer.is_valid():
                        raise Exception(f"Validation failed: {serializer.errors}")
                        
                    validated_data = serializer.validated_data
                    deductions_id = validated_data.get("id")
                    
                    if deductions_id is not None:
                        deductions = Deductions.objects.filter(id=deductions_id).first()
                        if not deductions:
                            raise Exception("Deductions not found!")
                    else:
                        deductions = Deductions()
                        
                    employee_id = validated_data.get("employeeId")
                    employee = CompanyEmployee.objects.filter(employeeId=employee_id).first()
                    if not employee:
                        raise Exception("Employee not found!")
                        
                    deductions.companyEmployee = employee
                    deductions.type = validated_data.get("type")
                    deductions.label = validated_data.get("label")
                    deductions.amount = validated_data.get("amount")
                    deductions.save()
        except Exception as e:
            logger.error(f"Error in save_deductions: {e}")
            raise Exception(str(e))

    def delete_by_id(self, id: int) -> None:
        try:
            deductions = Deductions.objects.filter(id=id).first()
            if not deductions:
                raise Exception("Deductions not found!")
            deductions.delete()
        except Exception as e:
            logger.error(f"Error in delete_by_id: {e}")
            raise Exception(str(e))

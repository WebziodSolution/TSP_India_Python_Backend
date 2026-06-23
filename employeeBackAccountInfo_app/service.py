import os
import logging
from common.models import EmployeeBackAccountInfo, CompanyEmployee
from common.serializers import EmployeeBackAccountInfoSerializer
from common.service import CommonService, get_file_directory

logger = logging.getLogger(__name__)

class EmployeeBankAccountInfoService:
    def __init__(self):
        self.common_service = CommonService()

    def get_bank_account_info_by_id(self, id: int) -> dict:
        try:
            entity = EmployeeBackAccountInfo.objects.filter(id=id).first()
            if not entity:
                raise Exception("Bank account info not found")
            dto = {
                "id": entity.id,
                "accountType": entity.accountType,
                "ifscCode": entity.ifscCode,
                "bankName": entity.bankName,
                "branch": entity.branch,
                "accountNumber": entity.accountNumber,
                "address": entity.address,
                "employeeId": entity.companyEmployee.employeeId if entity.companyEmployee else None,
                "passbookImage": entity.passbookImage
            }
            return EmployeeBackAccountInfoSerializer(dto).data
        except Exception as e:
            logger.error(f"Error in get_bank_account_info_by_id: {e}")
            raise Exception(str(e))

    def get_all_bank_account_info(self) -> list:
        try:
            entities = EmployeeBackAccountInfo.objects.all().order_by('id')
            dto_list = []
            for entity in entities:
                dto_list.append(self.get_bank_account_info_by_id(entity.id))
            return dto_list
        except Exception as e:
            logger.error(f"Error in get_all_bank_account_info: {e}")
            raise Exception(str(e))

    def create_bank_account_info(self, dto: dict) -> dict:
        try:
            serializer = EmployeeBackAccountInfoSerializer(data=dto)
            if not serializer.is_valid():
                raise Exception(f"Validation failed: {serializer.errors}")
                
            validated_data = serializer.validated_data
            employee_id = validated_data.get("employeeId")
            employee = CompanyEmployee.objects.filter(employeeId=employee_id).first()
            if not employee:
                raise Exception("Employee not found")
                
            entity = EmployeeBackAccountInfo(
                companyEmployee=employee,
                accountType=validated_data.get("accountType"),
                ifscCode=validated_data.get("ifscCode"),
                bankName=validated_data.get("bankName"),
                branch=validated_data.get("branch"),
                accountNumber=validated_data.get("accountNumber"),
                address=validated_data.get("address"),
                passbookImage=validated_data.get("passbookImage") or ""
            )
            entity.save()
            return self.get_bank_account_info_by_id(entity.id)
        except Exception as e:
            logger.error(f"Error in create_bank_account_info: {e}")
            raise Exception(str(e))

    def update_bank_account_info(self, id: int, dto: dict) -> dict:
        try:
            entity = EmployeeBackAccountInfo.objects.filter(id=id).first()
            if not entity:
                raise Exception("Bank account info not found")
                
            serializer = EmployeeBackAccountInfoSerializer(data=dto)
            if not serializer.is_valid():
                raise Exception(f"Validation failed: {serializer.errors}")
                
            validated_data = serializer.validated_data
            employee_id = validated_data.get("employeeId")
            employee = CompanyEmployee.objects.filter(employeeId=employee_id).first()
            if not employee:
                raise Exception("Employee not found")
                
            entity.companyEmployee = employee
            entity.accountType = validated_data.get("accountType")
            entity.ifscCode = validated_data.get("ifscCode")
            entity.bankName = validated_data.get("bankName")
            entity.branch = validated_data.get("branch")
            entity.accountNumber = validated_data.get("accountNumber")
            entity.address = validated_data.get("address")
            if validated_data.get("passbookImage") is not None:
                entity.passbookImage = validated_data.get("passbookImage")
            entity.save()
            return self.get_bank_account_info_by_id(entity.id)
        except Exception as e:
            logger.error(f"Error in update_bank_account_info: {e}")
            raise Exception(str(e))

    def delete_bank_account_info(self, id: int) -> None:
        try:
            entity = EmployeeBackAccountInfo.objects.filter(id=id).first()
            if not entity:
                raise Exception("Bank account info not found")
            entity.delete()
        except Exception as e:
            logger.error(f"Error in delete_bank_account_info: {e}")
            raise Exception(str(e))

    def upload_passbook_image(self, company_id: int, id: int, image_path: str) -> str:
        try:
            self.delete_passbook_image(company_id, id)
            entity = EmployeeBackAccountInfo.objects.filter(id=id).first()
            if not entity:
                raise Exception("Bank account info not found")
                
            updated_path = self.common_service.update_file_location_for_profile(
                image_path,
                company_id,
                f"employeeProfile/bank/{id}"
            )
            if updated_path == "Error":
                return "Error"
            else:
                entity.passbookImage = updated_path
                entity.save()
                return updated_path
        except Exception as e:
            logger.error(f"Error in upload_passbook_image: {e}")
            raise Exception(str(e))

    def delete_passbook_image(self, company_id: int, id: int) -> bool:
        try:
            entity = EmployeeBackAccountInfo.objects.filter(id=id).first()
            if not entity:
                raise Exception("Bank account info not found")
                
            file_dir = get_file_directory()
            existing_image_path = os.path.join(file_dir, str(company_id), "employeeProfile", "bank", str(id))
            if os.path.exists(existing_image_path):
                self.common_service.delete_directory_recursively(existing_image_path)
                entity.passbookImage = ""
                entity.save()
                return True
            return False
        except Exception as e:
            logger.error(f"Error in delete_passbook_image: {e}")
            raise Exception(str(e))

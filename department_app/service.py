import logging
from common.models import Department, CompanyDetails
from common.serializers import DepartmentSerializer

logger = logging.getLogger(__name__)

class DepartmentService:
    def get_department(self, id: int) -> dict:
        try:
            dept = Department.objects.filter(id=id).first()
            if not dept:
                raise Exception("Department not found")
            dto = {
                "id": dept.id,
                "companyId": dept.companyDetails.id if dept.companyDetails else None,
                "departmentName": dept.departmentName
            }
            return DepartmentSerializer(dto).data
        except Exception as e:
            logger.error(f"Error in get_department: {e}")
            raise Exception(str(e))

    def get_all_departments(self, company_id: int) -> list:
        try:
            departments = Department.objects.filter(companyDetails_id=company_id).order_by('id')
            dept_dto_list = []
            for d in departments:
                dept_dto_list.append(self.get_department(d.id))
            return dept_dto_list
        except Exception as e:
            logger.error(f"Error in get_all_departments: {e}")
            raise Exception(str(e))

    def create_department(self, department_dto: dict) -> dict:
        try:
            serializer = DepartmentSerializer(data=department_dto)
            if not serializer.is_valid():
                raise Exception(f"Validation failed: {serializer.errors}")
                
            validated_data = serializer.validated_data
            company_id = validated_data.get("companyId")
            company_details = None
            if company_id is not None:
                company_details = CompanyDetails.objects.filter(id=company_id).first()
                if not company_details:
                    raise Exception("Company not found")
                    
            dept = Department(
                departmentName=validated_data.get("departmentName"),
                companyDetails=company_details
            )
            dept.save()
            return self.get_department(dept.id)
        except Exception as e:
            logger.error(f"Error in create_department: {e}")
            raise Exception(str(e))

    def update_department(self, id: int, department_dto: dict) -> dict:
        try:
            dept = Department.objects.filter(id=id).first()
            if not dept:
                raise Exception("Department not found")
                
            serializer = DepartmentSerializer(data=department_dto)
            if not serializer.is_valid():
                raise Exception(f"Validation failed: {serializer.errors}")
                
            validated_data = serializer.validated_data
            company_id = validated_data.get("companyId")
            company_details = None
            if company_id is not None:
                company_details = CompanyDetails.objects.filter(id=company_id).first()
                if not company_details:
                    raise Exception("Company not found")
                    
            dept.departmentName = validated_data.get("departmentName")
            dept.companyDetails = company_details
            dept.save()
            return self.get_department(dept.id)
        except Exception as e:
            logger.error(f"Error in update_department: {e}")
            raise Exception(str(e))

    def delete_department(self, id: int) -> None:
        try:
            dept = Department.objects.filter(id=id).first()
            if not dept:
                raise Exception("Department not found")
            dept.delete()
        except Exception as e:
            logger.error(f"Error in delete_department: {e}")
            raise Exception(str(e))

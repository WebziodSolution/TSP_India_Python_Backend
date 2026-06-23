import logging
from django.db import transaction
from common.models import HolidayTemplates, CompanyDetails, CompanyEmployee
from common.serializers import HolidayTemplatesSerializer
from holidayTemplateDetails_app.service import HolidayTemplateDetailsService

logger = logging.getLogger(__name__)

class HolidayTemplatesService:
    def __init__(self):
        self.details_service = HolidayTemplateDetailsService()

    def get_holiday_template_by_id(self, id: int) -> dict:
        try:
            entity = HolidayTemplates.objects.filter(id=id).first()
            if not entity:
                raise Exception("Holiday Template not found")
            
            details_list = self.details_service.get_all_holiday_template_details_by_template_id(entity.id)
            assigned_emp_ids = self.get_assigned_employees(entity.id)
            
            dto = {
                "id": entity.id,
                "name": entity.name,
                "companyId": entity.companyDetails.id if entity.companyDetails else None,
                "createdBy": entity.companyEmployee.employeeId if entity.companyEmployee else None,
                "createdByUserName": entity.companyEmployee.userName if entity.companyEmployee else None,
                "holidayTemplateDetailsList": details_list,
                "assignedEmployeeIds": assigned_emp_ids
            }
            return HolidayTemplatesSerializer(dto).data
        except Exception as e:
            logger.error(f"Error in get_holiday_template_by_id: {e}")
            raise Exception(str(e))

    def get_all_holiday_templates_by_company_id(self, company_id: int) -> list:
        try:
            entities = HolidayTemplates.objects.filter(companyDetails_id=company_id).order_by('id')
            dto_list = []
            for entity in entities:
                dto_list.append(self.get_holiday_template_by_id(entity.id))
            return dto_list
        except Exception as e:
            logger.error(f"Error in get_all_holiday_templates_by_company_id: {e}")
            raise Exception(str(e))

    @transaction.atomic
    def create_holiday_template(self, dto: dict) -> dict:
        try:
            serializer = HolidayTemplatesSerializer(data=dto)
            if not serializer.is_valid():
                raise Exception(f"Validation failed: {serializer.errors}")
                
            validated_data = serializer.validated_data
            company_id = validated_data.get("companyId")
            company = CompanyDetails.objects.filter(id=company_id).first()
            if not company:
                raise Exception("Company not found")
                
            created_by = validated_data.get("createdBy")
            employee = CompanyEmployee.objects.filter(employeeId=created_by).first()
            if not employee:
                raise Exception("Company Employee not found")
                
            entity = HolidayTemplates(
                name=validated_data.get("name"),
                companyDetails=company,
                companyEmployee=employee
            )
            entity.save()
            
            details_list = validated_data.get("holidayTemplateDetailsList")
            if details_list and len(details_list) > 0:
                for details_dto in details_list:
                    # In DRF serializer, holidayTemplateDetailsList is parsed as list of dicts
                    details_dto["holidayTemplateId"] = entity.id
                    self.details_service.create_holiday_template_details(details_dto)
            else:
                raise Exception("Holiday list is required")
                
            return self.get_holiday_template_by_id(entity.id)
        except Exception as e:
            logger.error(f"Error in create_holiday_template: {e}")
            raise Exception(str(e))

    @transaction.atomic
    def update_holiday_template(self, id: int, dto: dict) -> dict:
        try:
            entity = HolidayTemplates.objects.filter(id=id).first()
            if not entity:
                raise Exception("Holiday Template not found")
                
            serializer = HolidayTemplatesSerializer(data=dto)
            if not serializer.is_valid():
                raise Exception(f"Validation failed: {serializer.errors}")
                
            validated_data = serializer.validated_data
            company_id = validated_data.get("companyId")
            company = CompanyDetails.objects.filter(id=company_id).first()
            if not company:
                raise Exception("Company not found")
                
            created_by = validated_data.get("createdBy")
            employee = CompanyEmployee.objects.filter(employeeId=created_by).first()
            if not employee:
                raise Exception("Company Employee not found")
                
            entity.name = validated_data.get("name")
            entity.companyDetails = company
            entity.companyEmployee = employee
            entity.save()
            
            details_list = validated_data.get("holidayTemplateDetailsList")
            if details_list and len(details_list) > 0:
                for details_dto in details_list:
                    detail_id = details_dto.get("id")
                    details_dto["holidayTemplateId"] = id
                    if detail_id is not None:
                        self.details_service.update_holiday_template_details(detail_id, details_dto)
                    else:
                        self.details_service.create_holiday_template_details(details_dto)
            else:
                raise Exception("Holiday list is required")
                
            return self.get_holiday_template_by_id(entity.id)
        except Exception as e:
            logger.error(f"Error in update_holiday_template: {e}")
            raise Exception(str(e))

    def delete_holiday_template(self, id: int) -> None:
        try:
            entity = HolidayTemplates.objects.filter(id=id).first()
            if not entity:
                raise Exception("Holiday Template not found")
            entity.delete()
        except Exception as e:
            logger.error(f"Error in delete_holiday_template: {e}")
            raise Exception(str(e))

    @transaction.atomic
    def assign_employees(self, template_id: int, employee_ids: list, remove_employee_ids: list) -> bool:
        try:
            template = HolidayTemplates.objects.filter(id=template_id).first()
            if not template:
                raise Exception("Holiday Template not found")
                
            if employee_ids:
                for emp_id in employee_ids:
                    employee = CompanyEmployee.objects.filter(employeeId=emp_id).first()
                    if not employee:
                        raise Exception("Company Employee not found")
                    employee.holidayTemplates = template
                    employee.save()
                    
            if remove_employee_ids:
                for emp_id in remove_employee_ids:
                    employee = CompanyEmployee.objects.filter(employeeId=emp_id).first()
                    if not employee:
                        raise Exception("Company Employee not found")
                    employee.holidayTemplates = None
                    employee.save()
                    
            return True
        except Exception as e:
            logger.error(f"Error in assign_employees: {e}")
            raise Exception(str(e))

    def get_assigned_employees(self, template_id: int) -> list:
        try:
            employees = CompanyEmployee.objects.filter(holidayTemplates_id=template_id)
            return [emp.employeeId for emp in employees]
        except Exception as e:
            logger.error(f"Error in get_assigned_employees: {e}")
            raise Exception(str(e))

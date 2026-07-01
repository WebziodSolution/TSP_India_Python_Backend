import logging
from common.models import LeaveType, CompanyDetails
from common.serializers import LeaveTypeSerializer

logger = logging.getLogger(__name__)

class LeaveTypeService:
    def get_leave_type(self, id: int) -> dict:
        try:
            lt = LeaveType.objects.filter(id=id).first()
            if not lt:
                raise Exception("LeaveType not found")
            dto = {
                "id": lt.id,
                "companyId": lt.companyDetails.id if lt.companyDetails else None,
                "name": lt.name
            }
            return LeaveTypeSerializer(dto).data
        except Exception as e:
            logger.error(f"Error in get_leave_type: {e}")
            raise Exception(str(e))

    def get_all_leave_types(self, company_id: int) -> list:
        try:
            leave_types = LeaveType.objects.filter(companyDetails_id=company_id).order_by('id')
            dto_list = []
            for lt in leave_types:
                dto_list.append(self.get_leave_type(lt.id))
            return dto_list
        except Exception as e:
            logger.error(f"Error in get_all_leave_types: {e}")
            raise Exception(str(e))

    def create_leave_type(self, leave_type_dto: dict) -> dict:
        try:
            serializer = LeaveTypeSerializer(data=leave_type_dto)
            if not serializer.is_valid():
                raise Exception(f"Validation failed: {serializer.errors}")
                
            validated_data = serializer.validated_data
            company_id = validated_data.get("companyId")
            company_details = None
            if company_id is not None:
                company_details = CompanyDetails.objects.filter(id=company_id).first()
                if not company_details:
                    raise Exception("Company not found")
                    
            lt = LeaveType(
                name=validated_data.get("name"),
                companyDetails=company_details
            )
            lt.save()
            return self.get_leave_type(lt.id)
        except Exception as e:
            logger.error(f"Error in create_leave_type: {e}")
            raise Exception(str(e))

    def update_leave_type(self, id: int, leave_type_dto: dict) -> dict:
        try:
            lt = LeaveType.objects.filter(id=id).first()
            if not lt:
                raise Exception("LeaveType not found")
                
            serializer = LeaveTypeSerializer(data=leave_type_dto)
            if not serializer.is_valid():
                raise Exception(f"Validation failed: {serializer.errors}")
                
            validated_data = serializer.validated_data
            company_id = validated_data.get("companyId")
            company_details = None
            if company_id is not None:
                company_details = CompanyDetails.objects.filter(id=company_id).first()
                if not company_details:
                    raise Exception("Company not found")
                    
            lt.name = validated_data.get("name")
            lt.companyDetails = company_details
            lt.save()
            return self.get_leave_type(lt.id)
        except Exception as e:
            logger.error(f"Error in update_leave_type: {e}")
            raise Exception(str(e))

    def delete_leave_type(self, id: int) -> None:
        try:
            lt = LeaveType.objects.filter(id=id).first()
            if not lt:
                raise Exception("LeaveType not found")
            lt.delete()
        except Exception as e:
            logger.error(f"Error in delete_leave_type: {e}")
            raise Exception(str(e))

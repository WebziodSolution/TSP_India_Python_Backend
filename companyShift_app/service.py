import logging
from common.models import CompanyShift, CompanyDetails
from common.serializers import CompanyShiftSerializer

logger = logging.getLogger(__name__)

class CompanyShiftService:
    def get_shift_by_id(self, id: int) -> dict:
        try:
            shift = CompanyShift.objects.filter(id=id).first()
            if not shift:
                raise Exception("Shift not found")
            dto = {
                "id": shift.id,
                "companyId": shift.companyDetails.id if shift.companyDetails else None,
                "shiftName": shift.shiftName,
                "shiftType": shift.shiftType,
                "startTime": shift.startTime,
                "endTime": shift.endTime,
                "hours": shift.hours,
                "totalHours": shift.totalHours
            }
            return CompanyShiftSerializer(dto).data
        except Exception as e:
            logger.error(f"Error in get_shift_by_id: {e}")
            raise Exception(str(e))

    def get_all_shifts(self, company_id: int) -> list:
        try:
            shifts = CompanyShift.objects.filter(companyDetails_id=company_id).order_by('id')
            shift_dto_list = []
            for shift in shifts:
                shift_dto_list.append(self.get_shift_by_id(shift.id))
            return shift_dto_list
        except Exception as e:
            logger.error(f"Error in get_all_shifts: {e}")
            raise Exception(str(e))

    def create_shift(self, company_shift_dto: dict) -> dict:
        try:
            serializer = CompanyShiftSerializer(data=company_shift_dto)
            if not serializer.is_valid():
                raise Exception(f"Validation failed: {serializer.errors}")
                
            validated_data = serializer.validated_data
            company_id = validated_data.get("companyId")
            company_details = CompanyDetails.objects.filter(id=company_id).first()
            if not company_details:
                raise Exception("Company not found")
                
            shift = CompanyShift(
                companyDetails=company_details,
                shiftName=validated_data.get("shiftName"),
                shiftType=validated_data.get("shiftType"),
                startTime=validated_data.get("startTime"),
                endTime=validated_data.get("endTime"),
                hours=validated_data.get("hours"),
                totalHours=validated_data.get("totalHours")
            )
            shift.save()
            return self.get_shift_by_id(shift.id)
        except Exception as e:
            logger.error(f"Error in create_shift: {e}")
            raise Exception(str(e))

    def update_shift(self, id: int, company_shift_dto: dict) -> dict:
        try:
            shift = CompanyShift.objects.filter(id=id).first()
            if not shift:
                raise Exception("Shift not found")
                
            serializer = CompanyShiftSerializer(data=company_shift_dto)
            if not serializer.is_valid():
                raise Exception(f"Validation failed: {serializer.errors}")
                
            validated_data = serializer.validated_data
            company_id = validated_data.get("companyId")
            company_details = CompanyDetails.objects.filter(id=company_id).first()
            if not company_details:
                raise Exception("Company not found")
                
            shift.companyDetails = company_details
            shift.shiftName = validated_data.get("shiftName")
            shift.shiftType = validated_data.get("shiftType")
            shift.startTime = validated_data.get("startTime")
            shift.endTime = validated_data.get("endTime")
            shift.hours = validated_data.get("hours")
            shift.totalHours = validated_data.get("totalHours")
            shift.save()
            return self.get_shift_by_id(shift.id)
        except Exception as e:
            logger.error(f"Error in update_shift: {e}")
            raise Exception(str(e))

    def delete_shift(self, id: int) -> None:
        try:
            shift = CompanyShift.objects.filter(id=id).first()
            if not shift:
                raise Exception("Shift not found")
            shift.delete()
        except Exception as e:
            logger.error(f"Error in delete_shift: {e}")
            raise Exception(str(e))

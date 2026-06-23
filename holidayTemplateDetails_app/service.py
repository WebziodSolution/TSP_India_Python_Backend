import logging
from common.models import HolidayTemplateDetails, HolidayTemplates
from common.serializers import HolidayTemplateDetailsSerializer
from common.service import CommonService

logger = logging.getLogger(__name__)

class HolidayTemplateDetailsService:
    def __init__(self):
        self.common_service = CommonService()

    def get_holiday_template_details_by_id(self, id: int) -> dict:
        try:
            entity = HolidayTemplateDetails.objects.filter(id=id).first()
            if not entity:
                raise Exception("Holiday Template Details not found")
            dto = {
                "id": entity.id,
                "name": entity.name,
                "holidayTemplateId": entity.holidayTemplates.id if entity.holidayTemplates else None,
                "date": self.common_service.convert_date_to_string(entity.date) if entity.date else None
            }
            return HolidayTemplateDetailsSerializer(dto).data
        except Exception as e:
            logger.error(f"Error in get_holiday_template_details_by_id: {e}")
            raise Exception(str(e))

    def get_all_holiday_template_details_by_template_id(self, id: int) -> list:
        try:
            entities = HolidayTemplateDetails.objects.filter(holidayTemplates_id=id).order_by('id')
            dto_list = []
            for entity in entities:
                dto_list.append(self.get_holiday_template_details_by_id(entity.id))
            return dto_list
        except Exception as e:
            logger.error(f"Error in get_all_holiday_template_details_by_template_id: {e}")
            raise Exception(str(e))

    def create_holiday_template_details(self, dto: dict) -> dict:
        try:
            serializer = HolidayTemplateDetailsSerializer(data=dto)
            if not serializer.is_valid():
                raise Exception(f"Validation failed: {serializer.errors}")
                
            validated_data = serializer.validated_data
            template_id = validated_data.get("holidayTemplateId")
            template = HolidayTemplates.objects.filter(id=template_id).first()
            if not template:
                raise Exception("Holiday Template not found")
                
            date_val = self.common_service.convert_string_to_date(validated_data.get("date"))
            
            entity = HolidayTemplateDetails(
                holidayTemplates=template,
                name=validated_data.get("name"),
                date=date_val
            )
            entity.save()
            return self.get_holiday_template_details_by_id(entity.id)
        except Exception as e:
            logger.error(f"Error in create_holiday_template_details: {e}")
            raise Exception(str(e))

    def update_holiday_template_details(self, id: int, dto: dict) -> dict:
        try:
            entity = HolidayTemplateDetails.objects.filter(id=id).first()
            if not entity:
                raise Exception("Holiday Template Details not found")
                
            serializer = HolidayTemplateDetailsSerializer(data=dto)
            if not serializer.is_valid():
                raise Exception(f"Validation failed: {serializer.errors}")
                
            validated_data = serializer.validated_data
            template_id = validated_data.get("holidayTemplateId")
            template = HolidayTemplates.objects.filter(id=template_id).first()
            if not template:
                raise Exception("Holiday Template not found")
                
            date_val = self.common_service.convert_string_to_date(validated_data.get("date"))
            
            entity.holidayTemplates = template
            entity.name = validated_data.get("name")
            entity.date = date_val
            entity.save()
            
            return self.get_holiday_template_details_by_id(entity.id)
        except Exception as e:
            logger.error(f"Error in update_holiday_template_details: {e}")
            raise Exception(str(e))

    def delete_holiday_template_details(self, id: int) -> None:
        try:
            entity = HolidayTemplateDetails.objects.filter(id=id).first()
            if not entity:
                raise Exception("Holiday Template Details not found")
            entity.delete()
        except Exception as e:
            logger.error(f"Error in delete_holiday_template_details: {e}")
            raise Exception(str(e))

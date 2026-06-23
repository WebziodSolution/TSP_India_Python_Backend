import logging
from common.models import CompanyFunctionality
from common.serializers import CompanyFunctionalitySerializer

logger = logging.getLogger(__name__)

class CompanyFunctionalityService:
    def get_all_functionality(self) -> list:
        try:
            items = CompanyFunctionality.objects.all()
            for item in items:
                item.functionalityId = item.id
            return CompanyFunctionalitySerializer(items, many=True).data
        except Exception as e:
            logger.error(f"Error get_all_functionality: {e}")
            raise Exception(str(e))

    def get_functionality(self, functionality_id: int) -> dict:
        try:
            item = CompanyFunctionality.objects.filter(id=functionality_id).first()
            if not item:
                raise Exception("Functionality not found")
            item.functionalityId = item.id
            return CompanyFunctionalitySerializer(item).data
        except Exception as e:
            logger.error(f"Error get_functionality: {e}")
            raise Exception(str(e))

    def create_functionality(self, data: dict) -> dict:
        try:
            serializer = CompanyFunctionalitySerializer(data=data)
            if not serializer.is_valid():
                raise Exception(f"Validation failed: {serializer.errors}")
                
            validated_data = serializer.validated_data
            item = CompanyFunctionality(
                functionalityName=validated_data.get("functionalityName") or ""
            )
            item.save()
            item.functionalityId = item.id
            return CompanyFunctionalitySerializer(item).data
        except Exception as e:
            logger.error(f"Error create_functionality: {e}")
            raise Exception(str(e))

    def update_functionality(self, functionality_id: int, data: dict) -> dict:
        try:
            item = CompanyFunctionality.objects.filter(id=functionality_id).first()
            if not item:
                raise Exception("Functionality not found")
                
            serializer = CompanyFunctionalitySerializer(data=data)
            if not serializer.is_valid():
                raise Exception(f"Validation failed: {serializer.errors}")
                
            validated_data = serializer.validated_data
            item.functionalityName = validated_data.get("functionalityName") or ""
            item.save()
            item.functionalityId = item.id
            return CompanyFunctionalitySerializer(item).data
        except Exception as e:
            logger.error(f"Error update_functionality: {e}")
            raise Exception(str(e))

    def delete_functionality(self, functionality_id: int) -> None:
        try:
            item = CompanyFunctionality.objects.filter(id=functionality_id).first()
            if not item:
                raise Exception("Functionality not found")
            item.delete()
        except Exception as e:
            logger.error(f"Error delete_functionality: {e}")
            raise Exception(str(e))

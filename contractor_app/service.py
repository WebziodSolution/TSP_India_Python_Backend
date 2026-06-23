import logging
from common.models import Contractor
from common.serializers import ContractorSerializer

logger = logging.getLogger(__name__)

class ContractorService:
    def get_contractor(self, id: int) -> dict:
        try:
            contractor = Contractor.objects.filter(id=id).first()
            if not contractor:
                raise Exception("Contractor not found")
            return ContractorSerializer(contractor).data
        except Exception as e:
            logger.error(f"Error in get_contractor: {e}")
            raise Exception(str(e))

    def get_all_contractors(self) -> list:
        try:
            contractors = Contractor.objects.all().order_by('id')
            contractor_dto_list = []
            for c in contractors:
                contractor_dto_list.append(self.get_contractor(c.id))
            return contractor_dto_list
        except Exception as e:
            logger.error(f"Error in get_all_contractors: {e}")
            raise Exception(str(e))

    def create_contractor(self, contractor_dto: dict) -> dict:
        try:
            serializer = ContractorSerializer(data=contractor_dto)
            if not serializer.is_valid():
                raise Exception(f"Validation failed: {serializer.errors}")
                
            validated_data = serializer.validated_data
            contractor = Contractor(
                contractorName=validated_data.get("contractorName")
            )
            contractor.save()
            return self.get_contractor(contractor.id)
        except Exception as e:
            logger.error(f"Error in create_contractor: {e}")
            raise Exception(str(e))

    def update_contractor(self, id: int, contractor_dto: dict) -> dict:
        try:
            contractor = Contractor.objects.filter(id=id).first()
            if not contractor:
                raise Exception("Contractor not found")
                
            serializer = ContractorSerializer(data=contractor_dto)
            if not serializer.is_valid():
                raise Exception(f"Validation failed: {serializer.errors}")
                
            validated_data = serializer.validated_data
            contractor.contractorName = validated_data.get("contractorName")
            contractor.save()
            return self.get_contractor(contractor.id)
        except Exception as e:
            logger.error(f"Error in update_contractor: {e}")
            raise Exception(str(e))

    def delete_contractor(self, id: int) -> None:
        try:
            contractor = Contractor.objects.filter(id=id).first()
            if not contractor:
                raise Exception("Contractor not found")
            contractor.delete()
        except Exception as e:
            logger.error(f"Error in delete_contractor: {e}")
            raise Exception(str(e))

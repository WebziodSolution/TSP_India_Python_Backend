import logging
from common.models import Functionality

logger = logging.getLogger(__name__)

class FunctionalityService:

    def _convert_model_to_dto(self, f: Functionality) -> dict:
        return {
            "functionalityId": f.id,
            "functionalityName": f.functionalityName
        }

    def getAllFunctionality(self) -> list:
        try:
            items = Functionality.objects.all().order_by('id')
            return [self._convert_model_to_dto(item) for item in items]
        except Exception as e:
            logger.error(f"Error getAllFunctionality: {e}")
            raise Exception(str(e))

    def getFunctionality(self, id_val: int) -> dict:
        try:
            f = Functionality.objects.filter(id=id_val).first()
            if not f:
                raise Exception("Functionality not found")
            return self._convert_model_to_dto(f)
        except Exception as e:
            logger.error(f"Error getFunctionality: {e}")
            raise Exception(str(e))

    def createFunctionality(self, dto: dict) -> dict:
        try:
            f = Functionality()
            f.functionalityName = dto.get("functionalityName")
            f.save()
            dto["functionalityId"] = f.id
            return dto
        except Exception as e:
            logger.error(f"Error createFunctionality: {e}")
            raise Exception(str(e))

    def updateFunctionality(self, id_val: int, dto: dict) -> dict:
        try:
            f = Functionality.objects.filter(id=id_val).first()
            if not f:
                raise Exception("Functionality not found")
            f.functionalityName = dto.get("functionalityName")
            f.save()
            dto["functionalityId"] = f.id
            return dto
        except Exception as e:
            logger.error(f"Error updateFunctionality: {e}")
            raise Exception(str(e))

    def deleteFunctionality(self, id_val: int) -> None:
        try:
            f = Functionality.objects.filter(id=id_val).first()
            if not f:
                raise Exception("Functionality not found")
            f.delete()
        except Exception as e:
            logger.error(f"Error deleteFunctionality: {e}")
            raise Exception(str(e))

import logging
from common.models import UserShift

logger = logging.getLogger(__name__)

class UserShiftService:

    def _convert_model_to_dto(self, user_shift: UserShift) -> dict:
        return {
            "id": user_shift.id,
            "shiftName": user_shift.shiftName
        }

    def getAllUserShift(self) -> list:
        try:
            user_shifts = UserShift.objects.all()
            return [self.getUserShift(shift.id) for shift in user_shifts]
        except Exception as e:
            logger.error(f"Error getAllUserShift: {e}")
            raise Exception(str(e))

    def getUserShift(self, id: int) -> dict:
        try:
            user_shift = UserShift.objects.filter(id=id).first()
            if not user_shift:
                raise Exception("Shift not found")
            return self._convert_model_to_dto(user_shift)
        except Exception as e:
            logger.error(f"Error getUserShift: {e}")
            raise Exception(str(e))

    def createUserShift(self, dto: dict) -> dict:
        try:
            user_shift = UserShift()
            user_shift.shiftName = dto.get("shiftName")
            user_shift.save()
            dto["id"] = user_shift.id
            return dto
        except Exception as e:
            logger.error(f"Error createUserShift: {e}")
            raise Exception(str(e))

    def updateUserShift(self, id: int, dto: dict) -> dict:
        try:
            user_shift = UserShift.objects.filter(id=id).first()
            if not user_shift:
                raise Exception("Shift not found")
            user_shift.shiftName = dto.get("shiftName")
            user_shift.save()
            dto["id"] = user_shift.id
            return dto
        except Exception as e:
            logger.error(f"Error updateUserShift: {e}")
            raise Exception(str(e))

    def deleteUserShift(self, id: int) -> None:
        try:
            user_shift = UserShift.objects.filter(id=id).first()
            if not user_shift:
                raise Exception("Shift not found")
            user_shift.delete()
        except Exception as e:
            logger.error(f"Error deleteUserShift: {e}")
            raise Exception(str(e))

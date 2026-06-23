import logging
from common.models.salarystatementmaster.salarystatementmaster import SalaryStatementMaster
from common.models.companydetails.companydetails import CompanyDetails

logger = logging.getLogger(__name__)

class SalaryStatementMasterService:
    def _to_dto(self, entity: SalaryStatementMaster) -> dict:
        return {
            "id": entity.id,
            "companyId": entity.companyDetails.id if entity.companyDetails else None,
            "month": entity.month,
            "year": entity.year,
            "totalSalary": entity.totalSalary,
            "totalPf": entity.totalPf,
            "totalPt": entity.totalPt,
            "note": entity.note,
        }

    def getAllSalaryStatementMasters(self, company_id: int) -> list:
        try:
            entities = SalaryStatementMaster.objects.filter(companyDetails_id=company_id)
            return [self._to_dto(e) for e in entities]
        except Exception as e:
            logger.error(f"Error in getAllSalaryStatementMasters: {e}")
            raise RuntimeError(e)

    def getSalaryStatementMastersByMonthAndYear(self, company_id: int, month: int, year: int) -> dict:
        try:
            entity = SalaryStatementMaster.objects.filter(
                companyDetails_id=company_id,
                month=month,
                year=year
            ).first()
            if entity:
                return self._to_dto(entity)
            return None
        except Exception as e:
            logger.error(f"Error in getSalaryStatementMastersByMonthAndYear: {e}")
            raise RuntimeError(e)

    def getSalaryStatementMasterById(self, id: int) -> dict:
        try:
            entity = SalaryStatementMaster.objects.filter(id=id).first()
            if not entity:
                raise Exception("Salary Statement Master not found")
            return self._to_dto(entity)
        except Exception as e:
            logger.error(f"Error in getSalaryStatementMasterById: {e}")
            raise RuntimeError(e)

    def createSalaryStatementMaster(self, dto: dict) -> dict:
        try:
            company_id = dto.get("companyId")
            company_details = CompanyDetails.objects.filter(id=company_id).first()
            if not company_details:
                raise Exception("Company not found")

            entity = SalaryStatementMaster(
                companyDetails=company_details,
                month=dto.get("month"),
                year=dto.get("year"),
                totalSalary=dto.get("totalSalary"),
                totalPf=dto.get("totalPf"),
                totalPt=dto.get("totalPt"),
                note=dto.get("note")
            )
            entity.save()
            return self._to_dto(entity)
        except Exception as e:
            logger.error(f"Error in createSalaryStatementMaster: {e}")
            raise RuntimeError(e)

    def updateSalaryStatementMaster(self, id: int, dto: dict) -> dict:
        try:
            entity = SalaryStatementMaster.objects.filter(id=id).first()
            if not entity:
                raise Exception("Salary Statement Master not found")

            company_id = dto.get("companyId")
            company_details = CompanyDetails.objects.filter(id=company_id).first()
            if not company_details:
                raise Exception("Company not found")

            entity.companyDetails = company_details
            entity.month = dto.get("month")
            entity.year = dto.get("year")
            entity.totalSalary = dto.get("totalSalary")
            entity.totalPf = dto.get("totalPf")
            entity.totalPt = dto.get("totalPt")
            entity.note = dto.get("note")
            entity.save()
            return self._to_dto(entity)
        except Exception as e:
            logger.error(f"Error in updateSalaryStatementMaster: {e}")
            raise RuntimeError(e)

    def deleteSalaryStatementMaster(self, id: int) -> None:
        try:
            entity = SalaryStatementMaster.objects.filter(id=id).first()
            if not entity:
                raise Exception("Salary Statement Master not found")
            entity.delete()
        except Exception as e:
            logger.error(f"Error in deleteSalaryStatementMaster: {e}")
            raise RuntimeError(e)

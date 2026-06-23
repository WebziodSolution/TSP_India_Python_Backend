import logging
from common.models import AttendancePenaltyRules, CompanyDetails, CompanyEmployee

logger = logging.getLogger(__name__)

class AttendancePenaltyRulesService:

    def _convert_model_to_dto(self, rule: AttendancePenaltyRules) -> dict:
        return {
            "id": rule.id,
            "ruleName": rule.ruleName,
            "companyId": rule.companyDetails.id if rule.companyDetails else None,
            "createdBy": rule.companyEmployee.employeeId if rule.companyEmployee else None,
            "createdByUserName": rule.companyEmployee.userName if rule.companyEmployee else None,
            "minutes": rule.minutes,
            "deductionType": rule.deductionType,
            "amount": rule.amount,
            "count": rule.count,
            "isEarlyExit": rule.isEarlyExit
        }

    def find_all_by_company_id(self, flag: int, company_id: int) -> list:
        try:
            is_early_exit = (flag == 1)
            rules = AttendancePenaltyRules.objects.filter(companyDetails_id=company_id, isEarlyExit=is_early_exit)
            return [self.find_by_id(rule.id) for rule in rules]
        except Exception as e:
            logger.error(f"Error find_all_by_company_id: {e}")
            raise Exception(str(e))

    def find_by_id(self, id: int) -> dict:
        try:
            rule = AttendancePenaltyRules.objects.filter(id=id).first()
            if not rule:
                raise Exception("Attendance penalty rule not found")
            return self._convert_model_to_dto(rule)
        except Exception as e:
            logger.error(f"Error find_by_id: {e}")
            raise Exception(str(e))

    def create(self, dto: dict) -> dict:
        try:
            rule_name = dto.get("ruleName")
            company_id = dto.get("companyId")
            is_early_exit = dto.get("isEarlyExit", False)
            minutes = dto.get("minutes")

            # Check duplication by name
            existing_rule = AttendancePenaltyRules.objects.filter(
                ruleName=rule_name,
                companyDetails_id=company_id,
                isEarlyExit=is_early_exit
            ).first()
            if existing_rule:
                raise Exception(f"Penalty rule already exists with name {rule_name}")

            # Check duplication by minutes
            existing_rule_with_minutes = AttendancePenaltyRules.objects.filter(
                minutes=minutes,
                companyDetails_id=company_id,
                isEarlyExit=is_early_exit
            ).first()
            if existing_rule_with_minutes:
                raise Exception(f"Penalty rule already exists for {minutes} minutes")

            # Find company
            company = CompanyDetails.objects.filter(id=company_id).first()
            if not company:
                raise Exception("Company not found")

            # Find employee (createdBy)
            created_by = dto.get("createdBy")
            employee = CompanyEmployee.objects.filter(employeeId=created_by).first()
            if not employee:
                raise Exception("Company employee not found")

            # Create rule object
            rule = AttendancePenaltyRules()
            rule.companyDetails = company
            rule.companyEmployee = employee
            rule.ruleName = rule_name
            rule.minutes = minutes
            rule.deductionType = dto.get("deductionType")
            rule.amount = dto.get("amount")
            rule.count = dto.get("count")
            rule.isEarlyExit = is_early_exit
            rule.save()

            return self._convert_model_to_dto(rule)
        except Exception as e:
            logger.error(f"Error create: {e}")
            raise Exception(str(e))

    def update(self, id: int, dto: dict) -> dict:
        try:
            rule_name = dto.get("ruleName")
            company_id = dto.get("companyId")
            is_early_exit = dto.get("isEarlyExit", False)
            minutes = dto.get("minutes")

            # Check duplication by name excluding current ID
            existing_rule = AttendancePenaltyRules.objects.filter(
                ruleName=rule_name,
                companyDetails_id=company_id,
                isEarlyExit=is_early_exit
            ).exclude(id=id).first()
            if existing_rule:
                raise Exception(f"Penalty rule already exists with name {rule_name}")

            # Check duplication by minutes excluding current ID
            existing_rule_with_minutes = AttendancePenaltyRules.objects.filter(
                minutes=minutes,
                companyDetails_id=company_id,
                isEarlyExit=is_early_exit
            ).exclude(id=id).first()
            if existing_rule_with_minutes:
                raise Exception(f"Penalty rule already exists for {minutes} minutes")

            # Get the penalty rule to update
            rule = AttendancePenaltyRules.objects.filter(id=id).first()
            if not rule:
                raise Exception("Penalty rule not found")

            # Find company
            company = CompanyDetails.objects.filter(id=company_id).first()
            if not company:
                raise Exception("Company not found")

            # Find employee (createdBy)
            created_by = dto.get("createdBy")
            if created_by:
                employee = CompanyEmployee.objects.filter(employeeId=created_by).first()
                if not employee:
                    raise Exception("Company employee not found")
                rule.companyEmployee = employee

            rule.companyDetails = company
            rule.ruleName = rule_name
            rule.minutes = minutes
            rule.deductionType = dto.get("deductionType")
            rule.amount = dto.get("amount")
            rule.count = dto.get("count")
            rule.isEarlyExit = is_early_exit
            rule.save()

            return self._convert_model_to_dto(rule)
        except Exception as e:
            logger.error(f"Error update: {e}")
            raise Exception(str(e))

    def delete_by_id(self, id: int) -> None:
        try:
            rule = AttendancePenaltyRules.objects.filter(id=id).first()
            if not rule:
                raise Exception("Penalty rule not found")
            rule.delete()
        except Exception as e:
            logger.error(f"Error delete_by_id: {e}")
            raise Exception(str(e))

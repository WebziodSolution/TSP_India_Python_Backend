import logging
from common.models import OvertimeRules, CompanyDetails, CompanyEmployee

logger = logging.getLogger(__name__)

class OvertimeRulesService:

    def _convert_model_to_dto(self, rule: OvertimeRules) -> dict:
        return {
            "id": rule.id,
            "ruleName": rule.ruleName,
            "otMinutes": rule.otMinutes,
            "otAmount": rule.otAmount,
            "otType": rule.otType,
            "companyId": rule.companyDetails.id if rule.companyDetails else None,
            "createdBy": rule.companyEmployee.employeeId if rule.companyEmployee else None,
            "createdByUserName": rule.companyEmployee.userName if rule.companyEmployee else None
        }

    def get_all_overtime_rules(self, company_id: int) -> list:
        try:
            rules_list = OvertimeRules.objects.filter(companyDetails_id=company_id)
            return [self.get_overtime_rule(rule.id) for rule in rules_list]
        except Exception as e:
            logger.error(f"Error get_all_overtime_rules: {e}")
            raise Exception(str(e))

    def get_overtime_rule(self, id: int) -> dict:
        try:
            rule = OvertimeRules.objects.filter(id=id).first()
            if not rule:
                raise Exception("Overtime rule not found with id: " + str(id))
            return self._convert_model_to_dto(rule)
        except Exception as e:
            logger.error(f"Error get_overtime_rule: {e}")
            raise Exception(str(e))

    def _find_duplicate_rule_name(self, id_val, rule_name: str, company_id: int) -> bool:
        if id_val is None:
            return OvertimeRules.objects.filter(ruleName=rule_name, companyDetails_id=company_id).exists()
        return OvertimeRules.objects.filter(ruleName=rule_name, companyDetails_id=company_id).exclude(id=id_val).exists()

    def create_overtime_rule(self, dto: dict, company_id: int) -> dict:
        try:
            rule_name = dto.get("ruleName")
            if self._find_duplicate_rule_name(None, rule_name, company_id):
                raise Exception(f"Overtime rule with name '{rule_name}' already exists.")

            company = CompanyDetails.objects.filter(id=company_id).first()
            if not company:
                raise Exception("Company not found with id: " + str(company_id))

            created_by = dto.get("createdBy")
            employee = CompanyEmployee.objects.filter(employeeId=created_by).first()
            if not employee:
                raise Exception("Company employee not found")

            rule = OvertimeRules()
            rule.companyDetails = company
            rule.companyEmployee = employee
            rule.ruleName = rule_name
            rule.otMinutes = dto.get("otMinutes")
            rule.otAmount = dto.get("otAmount")
            rule.otType = dto.get("otType")
            rule.save()

            saved_dto = self._convert_model_to_dto(rule)
            return saved_dto
        except Exception as e:
            logger.error(f"Error create_overtime_rule: {e}")
            raise Exception(str(e))

    def update_overtime_rule(self, id: int, dto: dict) -> dict:
        try:
            company_id = dto.get("companyId")
            rule_name = dto.get("ruleName")
            if self._find_duplicate_rule_name(id, rule_name, company_id):
                raise Exception(f"Overtime rule with name '{rule_name}' already exists.")

            rule = OvertimeRules.objects.filter(id=id).first()
            if not rule:
                raise Exception("Overtime rule not found")

            company = CompanyDetails.objects.filter(id=company_id).first()
            if not company:
                raise Exception("Company not found")

            created_by = dto.get("createdBy")
            employee = CompanyEmployee.objects.filter(employeeId=created_by).first()
            if not employee:
                raise Exception("Company employee not found")

            rule.companyDetails = company
            rule.companyEmployee = employee
            rule.ruleName = rule_name
            rule.otMinutes = dto.get("otMinutes")
            rule.otAmount = dto.get("otAmount")
            rule.otType = dto.get("otType")
            rule.save()

            saved_dto = self._convert_model_to_dto(rule)
            return saved_dto
        except Exception as e:
            logger.error(f"Error update_overtime_rule: {e}")
            raise Exception(str(e))

    def delete_overtime_rule(self, id: int) -> None:
        try:
            rule = OvertimeRules.objects.filter(id=id).first()
            if not rule:
                raise Exception("Overtime rule not found")
            rule.delete()
        except Exception as e:
            logger.error(f"Error delete_overtime_rule: {e}")
            raise Exception(str(e))

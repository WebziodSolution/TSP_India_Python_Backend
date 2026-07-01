import logging
import pytz
from datetime import datetime, time
from django.db.models import Q, Sum
from common.models.salarystatementhistory.salarystatementhistory import SalaryStatementHistory
from common.models.companydetails.companydetails import CompanyDetails
from common.models.companyemployee.companyemployee import CompanyEmployee
from common.models.userinout.userinout import UserInOut
from common.models import EmployeeLeaveMaster
from common.service import CommonService

logger = logging.getLogger(__name__)
common_service = CommonService()

class SalaryStatementHistoryService:
    def _parse_month_year(self, month_year_str: str) -> datetime:
        try:
            return datetime.strptime(month_year_str, "%B-%Y")
        except Exception:
            return datetime.min

    def _to_dto(self, entity: SalaryStatementHistory) -> dict:
        return {
            "id": entity.id,
            "clockInOutId": entity.clockInOutId,
            "companyId": entity.companyDetails.id if entity.companyDetails else None,
            "employeeId": entity.employeeId,
            "employeeName": entity.employeeName,
            "departmentId": entity.departmentId,
            "departmentName": entity.departmentName,
            "basicSalary": entity.basicSalary,
            "totalEarnSalary": entity.totalEarnSalary,
            "otAmount": entity.otAmount,
            "pfAmount": entity.pfAmount,
            "totalPfAmount": entity.totalPfAmount,
            "pfPercentage": entity.pfPercentage,
            "ptAmount": entity.ptAmount,
            "totalEarnings": entity.totalEarnings,
            "totalPenaltyAmount": entity.totalPenaltyAmount,
            "otherDeductions": entity.otherDeductions,
            "totalDeductions": entity.totalDeductions,
            "netSalary": entity.netSalary,
            "year": entity.year,
            "monthNumber": entity.month,
            "monthYear": entity.monthYear,
            "totalPaidDays": entity.totalPaidDays,
            "totalWorkingDays": entity.totalWorkingDays,
            "totalWorkingHours": entity.totalWorkingHours,
            "totalDays": entity.totalDays,
            "startDate": None,
            "endDate": None,
            "timeZone": None,
            "note": entity.note,
            "generatedBy": entity.companyEmployee.employeeId if entity.companyEmployee else None,
            "deductionsList": self.calculateTotalAllowanceAndDeductions(entity.employeeId, "Deduction"),
            "allowanceList": self.calculateTotalAllowanceAndDeductions(entity.employeeId, "Allowance"),
            "used_leave": EmployeeLeaveMaster.objects.filter(companyEmployee_id=entity.employeeId).values_list('usedLeave', flat=True).first(),
        }

    def calculateTotalAllowanceAndDeductions(self, user_id: int, type_str: str) -> list:
        if not user_id:
            return []
        from common.models.deductions.deductions import Deductions
        deductions = Deductions.objects.filter(companyEmployee_id=user_id, type=type_str)
        return [
            {
                "label": d.label,
                "amount": d.amount,
                "type": d.type
            } for d in deductions
        ]

    def _to_start_of_day_utc(self, dt: datetime) -> datetime:
        if not dt:
            return None
        return datetime.combine(dt.date(), time.min).replace(tzinfo=pytz.UTC)

    def _to_end_of_day_utc(self, dt: datetime) -> datetime:
        if not dt:
            return None
        return datetime.combine(dt.date(), time.max).replace(tzinfo=pytz.UTC)

    def filterSalaryStatementHistory(self, employee_ids: list, department_ids: list, months: list, company_id: int) -> list:
        try:
            if not employee_ids and not department_ids and not months:
                logger.info("All filters are empty, returning empty list.")
                return []

            query = Q()
            if company_id and company_id > 0:
                query &= Q(companyDetails_id=company_id)
            if employee_ids:
                query &= Q(employeeId__in=employee_ids)
            if department_ids:
                query &= Q(departmentId__in=department_ids)
            if months:
                query &= Q(monthYear__in=months)

            entities = SalaryStatementHistory.objects.filter(query)
            dto_list = [self.getSalaryStatementHistory(entity.id) for entity in entities]

            # Group by monthYear
            grouped = {}
            for dto in dto_list:
                m_y = dto.get("monthYear") or ""
                if m_y not in grouped:
                    grouped[m_y] = []
                grouped[m_y].append(dto)

            # Sort groups by parsed monthYear
            sorted_keys = sorted(grouped.keys(), key=self._parse_month_year)
            result = []
            for k in sorted_keys:
                result.append({
                    "month": k,
                    "data": grouped[k]
                })

            return result
        except Exception as e:
            logger.error(f"Error in filterSalaryStatementHistory: {e}")
            raise RuntimeError(e)

    def getSalaryStatementHistory(self, id: int) -> dict:
        try:
            entity = SalaryStatementHistory.objects.filter(id=id).first()
            if not entity:
                raise Exception("Salary Statement History not found")
            return self._to_dto(entity)
        except Exception as e:
            logger.error(f"Error in getSalaryStatementHistory: {e}")
            raise RuntimeError(e)

    def addSalaryStatement(self, salary_statement_list: list) -> dict:
        try:
            def add_val(val1, val2):
                return (val1 or 0) + (val2 or 0)

            for dto in salary_statement_list:
                start_date_raw = common_service.convert_string_to_date(dto.get("startDate"))
                end_date_raw = common_service.convert_string_to_date(dto.get("endDate"))

                start_date = self._to_start_of_day_utc(start_date_raw)
                end_date = self._to_end_of_day_utc(end_date_raw)

                # Update UserInOut status
                if start_date and end_date:
                    user_in_outs = UserInOut.objects.filter(
                        user_id=dto.get("employeeId"),
                        createdOn__gte=start_date,
                        createdOn__lte=end_date
                    )
                    for uio in user_in_outs:
                        uio.isSalaryGenerate = 1
                        uio.save()

                # Update EmployeeLeaveMaster usedLeave
                used_leave_val = dto.get("used_leave")
                if used_leave_val is not None:
                    elm = EmployeeLeaveMaster.objects.filter(companyEmployee_id=dto.get("employeeId")).first()
                    if elm:
                        elm.usedLeave = used_leave_val
                        elm.save()

                entity = SalaryStatementHistory.objects.filter(
                    employeeId=dto.get("employeeId"),
                    companyDetails_id=dto.get("companyId"),
                    month=dto.get("monthNumber"),
                    year=dto.get("year")
                ).first()

                if entity:
                    entity.otAmount = add_val(dto.get("otAmount"), entity.otAmount)
                    entity.totalEarnSalary = add_val(dto.get("totalEarnings"), entity.totalEarnSalary)
                    entity.totalPfAmount = add_val(dto.get("totalPfAmount"), entity.totalPfAmount)
                    entity.ptAmount = add_val(dto.get("ptAmount"), entity.ptAmount)
                    entity.netSalary = add_val(dto.get("netSalary"), entity.netSalary)
                    entity.otherDeductions = add_val(dto.get("otherDeductions"), entity.otherDeductions)
                    entity.totalDeductions = add_val(dto.get("totalDeductions"), entity.totalDeductions)
                    entity.totalEarnings = add_val(dto.get("totalEarnings"), entity.totalEarnings)
                    entity.totalPenaltyAmount = add_val(dto.get("totalPenaltyAmount"), entity.totalPenaltyAmount)
                    entity.note = dto.get("note")
                    entity.save()
                else:
                    entity = SalaryStatementHistory()
                    company_details = CompanyDetails.objects.filter(id=dto.get("companyId")).first()
                    if not company_details:
                        raise Exception("Company not found")
                    entity.companyDetails = company_details

                    company_employee = CompanyEmployee.objects.filter(employeeId=dto.get("generatedBy")).first()
                    if not company_employee:
                        raise Exception("Company Employee not found")
                    entity.companyEmployee = company_employee

                    entity.clockInOutId = int(dto.get("clockInOutId")) if dto.get("clockInOutId") is not None else None
                    entity.month = dto.get("monthNumber")
                    entity.year = dto.get("year")
                    entity.generatedDate = datetime.now().date()

                    entity.employeeId = dto.get("employeeId")
                    entity.employeeName = dto.get("employeeName")
                    entity.departmentId = dto.get("departmentId")
                    entity.departmentName = dto.get("departmentName")
                    entity.basicSalary = dto.get("basicSalary")
                    entity.totalEarnSalary = dto.get("totalEarnSalary")
                    entity.otAmount = dto.get("otAmount")
                    entity.pfAmount = dto.get("pfAmount")
                    entity.totalPfAmount = dto.get("totalPfAmount")
                    entity.pfPercentage = dto.get("pfPercentage")
                    entity.ptAmount = dto.get("ptAmount")
                    entity.totalEarnings = dto.get("totalEarnings")
                    entity.totalPenaltyAmount = dto.get("totalPenaltyAmount")
                    entity.otherDeductions = dto.get("otherDeductions")
                    entity.totalDeductions = dto.get("totalDeductions")
                    entity.netSalary = dto.get("netSalary")
                    entity.monthYear = dto.get("monthYear")
                    entity.totalPaidDays = dto.get("totalPaidDays")
                    entity.totalWorkingDays = dto.get("totalWorkingDays")
                    entity.totalWorkingHours = dto.get("totalWorkingHours")
                    entity.totalDays = dto.get("totalDays")
                    entity.note = dto.get("note")
                    entity.save()

                # Update or Create SalaryStatementMaster
                from salaryStatementMaster_app.service import SalaryStatementMasterService
                master_service = SalaryStatementMasterService()

                master_dto = master_service.getSalaryStatementMastersByMonthAndYear(
                    dto.get("companyId"), dto.get("monthNumber"), dto.get("year")
                )

                if master_dto:
                    total_salary = add_val(dto.get("netSalary"), master_dto.get("totalSalary")) if master_dto.get("totalSalary") is not None else 0
                    master_dto["totalSalary"] = total_salary

                    pf_amount = add_val(dto.get("totalPfAmount"), master_dto.get("totalPf")) if master_dto.get("totalPf") is not None else 0
                    master_dto["totalPf"] = pf_amount

                    pt_amount = add_val(dto.get("ptAmount"), master_dto.get("totalPt")) if master_dto.get("totalPt") is not None else 0
                    master_dto["totalPt"] = pt_amount

                    master_dto["note"] = master_dto.get("note")

                    master_service.updateSalaryStatementMaster(master_dto.get("id"), master_dto)
                else:
                    first_dto = salary_statement_list[0]
                    new_master_dto = {
                        "companyId": first_dto.get("companyId"),
                        "month": first_dto.get("monthNumber"),
                        "year": first_dto.get("year"),
                        "note": dto.get("note"),
                        "totalSalary": dto.get("netSalary"),
                        "totalPf": dto.get("totalPfAmount"),
                        "totalPt": dto.get("ptAmount")
                    }
                    master_service.createSalaryStatementMaster(new_master_dto)

            return {}
        except Exception as e:
            logger.error(f"Error in addSalaryStatement: {e}")
            raise RuntimeError(e)

    def updateSalaryStatement(self, id: int, dto: dict) -> dict:
        try:
            entity = SalaryStatementHistory.objects.filter(id=id).first()
            if not entity:
                raise Exception("Salary Statement History not found")

            company_id = dto.get("companyId")
            company_details = CompanyDetails.objects.filter(id=company_id).first()
            if not company_details:
                raise Exception("Company not found")
            entity.companyDetails = company_details

            generated_by = dto.get("generatedBy")
            company_employee = CompanyEmployee.objects.filter(employeeId=generated_by).first() if generated_by else None
            entity.companyEmployee = company_employee

            entity.clockInOutId = int(dto.get("clockInOutId")) if dto.get("clockInOutId") is not None else None
            entity.month = dto.get("monthNumber")
            entity.year = dto.get("year")

            entity.employeeId = dto.get("employeeId")
            entity.employeeName = dto.get("employeeName")
            entity.departmentId = dto.get("departmentId")
            entity.departmentName = dto.get("departmentName")
            entity.basicSalary = dto.get("basicSalary")
            entity.totalEarnSalary = dto.get("totalEarnSalary")
            entity.otAmount = dto.get("otAmount")
            entity.pfAmount = dto.get("pfAmount")
            entity.totalPfAmount = dto.get("totalPfAmount")
            entity.pfPercentage = dto.get("pfPercentage")
            entity.ptAmount = dto.get("ptAmount")
            entity.totalEarnings = dto.get("totalEarnings")
            entity.totalPenaltyAmount = dto.get("totalPenaltyAmount")
            entity.otherDeductions = dto.get("otherDeductions")
            entity.totalDeductions = dto.get("totalDeductions")
            entity.netSalary = dto.get("netSalary")
            entity.monthYear = dto.get("monthYear")
            entity.totalPaidDays = dto.get("totalPaidDays")
            entity.totalWorkingDays = dto.get("totalWorkingDays")
            entity.totalWorkingHours = dto.get("totalWorkingHours")
            entity.totalDays = dto.get("totalDays")
            entity.note = dto.get("note")

            entity.save()

            # Aggregate totals
            totals = SalaryStatementHistory.objects.filter(
                companyDetails_id=dto.get("companyId"),
                month=dto.get("monthNumber"),
                year=dto.get("year")
            ).aggregate(
                total_net=Sum('netSalary'),
                total_pf=Sum('totalPfAmount'),
                total_pt=Sum('ptAmount')
            )

            totalNetSalary = totals.get("total_net") or 0
            totalPfAmount = totals.get("total_pf") or 0
            totalPtAmount = totals.get("total_pt") or 0

            from salaryStatementMaster_app.service import SalaryStatementMasterService
            master_service = SalaryStatementMasterService()

            master_dto = master_service.getSalaryStatementMastersByMonthAndYear(
                dto.get("companyId"), dto.get("monthNumber"), dto.get("year")
            )
            if master_dto:
                master_dto["totalSalary"] = totalNetSalary
                master_dto["totalPf"] = totalPfAmount
                master_dto["totalPt"] = totalPtAmount
                master_service.updateSalaryStatementMaster(master_dto.get("id"), master_dto)

            return dto
        except Exception as e:
            logger.error(f"Error in updateSalaryStatement: {e}")
            raise RuntimeError(e)

    def deleteSalaryStatement(self, id: int) -> None:
        try:
            entity = SalaryStatementHistory.objects.filter(id=id).first()
            if not entity:
                raise Exception("Salary Statement History not found")
            entity.delete()
        except Exception as e:
            logger.error(f"Error in deleteSalaryStatement: {e}")
            raise RuntimeError(e)
